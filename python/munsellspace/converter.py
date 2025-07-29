"""
MunsellSpace color converter implementation.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Union, Tuple

from .types import MunsellColor, ConversionError


class MunsellConverter:
    """
    High-precision sRGB to Munsell color space converter.
    
    This class provides a Python interface to the Rust MunsellSpace library,
    offering 99.98% accuracy on the complete reference dataset (4,006/4,007 exact matches).
    
    Features:
        * 99.98% accuracy on reference dataset (4,006/4,007 exact matches)
        * 4,000+ colors/second batch processing performance
        * Scientific precision with intelligent interpolation
        * Zero external dependencies (uses bundled Rust binary)
        * Comprehensive error handling and validation
    
    The converter uses the Rust MunsellSpace library via JSON IPC for optimal
    performance while maintaining the safety and accuracy of the Rust implementation.
    
    Examples:
        >>> converter = MunsellConverter()
        >>> 
        >>> # Single color conversion
        >>> red = converter.srgb_to_munsell([255, 0, 0])
        >>> print(red)  # 7.9R 5.2/20.5
        >>> 
        >>> # Batch processing for better performance
        >>> colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
        >>> results = converter.convert_batch(colors)
        >>> for color, result in zip(colors, results):
        ...     print(f"RGB{color} -> {result}")
        
    Note:
        The converter automatically locates and uses the appropriate Rust binary
        for your platform. On first use, it may take slightly longer as the
        binary initializes its reference data.
    """
    
    def __init__(self, binary_path: Union[str, Path, None] = None):
        """
        Initialize the Munsell converter.
        
        Args:
            binary_path (Union[str, Path, None], optional): 
                Path to the Rust binary. If None, will attempt to locate
                the binary automatically. Defaults to None.
                
        Raises:
            ConversionError: If the Rust binary cannot be found or initialized
        """
        self._binary_path = self._find_binary(binary_path)
        self._validate_binary()
    
    def _find_binary(self, binary_path: Union[str, Path, None]) -> Path:
        """Find the Rust binary for color conversion."""
        if binary_path:
            path = Path(binary_path)
            if path.exists():
                return path
            raise ConversionError(f"Binary not found at specified path: {binary_path}")
        
        # Try to find the binary in the package directory
        package_dir = Path(__file__).parent
        possible_paths = [
            package_dir / "bin" / "munsellspace",
            package_dir / "bin" / "munsellspace.exe",  # Windows
            package_dir.parent.parent / "target" / "release" / "munsellspace",  # Development
            package_dir.parent.parent / "target" / "release" / "munsellspace.exe",  # Windows dev
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # Try system PATH
        try:
            result = subprocess.run(["which", "munsellspace"], 
                                  capture_output=True, text=True, check=True)
            return Path(result.stdout.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        raise ConversionError(
            "MunsellSpace Rust binary not found. Please ensure the package was installed correctly "
            "or provide the binary_path parameter."
        )
    
    def _validate_binary(self) -> None:
        """Validate that the binary works correctly."""
        try:
            # Test with a simple conversion
            result = subprocess.run(
                [str(self._binary_path), "--test"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise ConversionError(f"Binary validation failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            raise ConversionError("Binary validation timed out")
        except Exception as e:
            raise ConversionError(f"Binary validation error: {e}")
    
    def srgb_to_munsell(self, rgb: List[int]) -> MunsellColor:
        """
        Convert a single sRGB color to Munsell notation.
        
        Args:
            rgb (List[int]): RGB color as [R, G, B] where each component 
                is in the range 0-255.
                
        Returns:
            MunsellColor: The converted color in Munsell notation
            
        Raises:
            ConversionError: If the RGB values are invalid or conversion fails
            
        Examples:
            >>> converter = MunsellConverter()
            >>> red = converter.srgb_to_munsell([255, 0, 0])
            >>> print(red.notation)  # "7.9R 5.2/20.5"
            >>> print(red.hue)       # "7.9R"
            >>> print(red.value)     # 5.2
            >>> print(red.chroma)    # 20.5
            >>> 
            >>> # Neutral color
            >>> gray = converter.srgb_to_munsell([128, 128, 128])
            >>> print(gray.notation)  # "N 5.6/"
            >>> print(gray.is_neutral())  # True
        """
        self._validate_rgb(rgb)
        
        try:
            # Call Rust binary with JSON input
            input_data = {"rgb": rgb}
            result = subprocess.run(
                [str(self._binary_path), "--json"],
                input=json.dumps(input_data),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                raise ConversionError(f"Conversion failed: {result.stderr}")
            
            # Parse the result
            output = json.loads(result.stdout)
            if "error" in output:
                raise ConversionError(f"Conversion error: {output['error']}")
            
            return MunsellColor.from_notation(output["munsell"])
            
        except json.JSONDecodeError as e:
            raise ConversionError(f"Invalid response from conversion binary: {e}")
        except subprocess.TimeoutExpired:
            raise ConversionError("Conversion timed out")
        except Exception as e:
            raise ConversionError(f"Unexpected conversion error: {e}")
    
    def convert_batch(self, rgb_colors: List[List[int]]) -> List[MunsellColor]:
        """
        Convert multiple sRGB colors to Munsell notation efficiently.
        
        This method is more efficient than calling srgb_to_munsell() multiple times
        as it reduces the overhead of process startup and JSON parsing.
        
        Args:
            rgb_colors (List[List[int]]): List of RGB colors, where each color
                is [R, G, B] with components in the range 0-255.
                
        Returns:
            List[MunsellColor]: List of converted colors in Munsell notation
            
        Raises:
            ConversionError: If any RGB values are invalid or conversion fails
            
        Examples:
            >>> converter = MunsellConverter()
            >>> colors = [
            ...     [255, 0, 0],    # Red
            ...     [0, 255, 0],    # Green
            ...     [0, 0, 255],    # Blue
            ...     [128, 128, 128] # Gray
            ... ]
            >>> results = converter.convert_batch(colors)
            >>> for rgb, munsell in zip(colors, results):
            ...     print(f"RGB{rgb} -> {munsell}")
            
        Performance:
            Batch processing achieves 4,000+ colors/second, significantly
            faster than individual conversions for large datasets.
        """
        # Validate all RGB values first
        for i, rgb in enumerate(rgb_colors):
            try:
                self._validate_rgb(rgb)
            except ConversionError as e:
                raise ConversionError(f"Invalid RGB at index {i}: {e}")
        
        if not rgb_colors:
            return []
        
        try:
            # Call Rust binary with batch JSON input
            input_data = {"batch": rgb_colors}
            result = subprocess.run(
                [str(self._binary_path), "--batch", "--json"],
                input=json.dumps(input_data),
                capture_output=True,
                text=True,
                timeout=max(10, len(rgb_colors) // 100)  # Scale timeout with batch size
            )
            
            if result.returncode != 0:
                raise ConversionError(f"Batch conversion failed: {result.stderr}")
            
            # Parse the results
            output = json.loads(result.stdout)
            if "error" in output:
                raise ConversionError(f"Batch conversion error: {output['error']}")
            
            if "results" not in output:
                raise ConversionError("Invalid batch response format")
            
            results = []
            for i, munsell_notation in enumerate(output["results"]):
                if isinstance(munsell_notation, dict) and "error" in munsell_notation:
                    raise ConversionError(f"Conversion error at index {i}: {munsell_notation['error']}")
                results.append(MunsellColor.from_notation(munsell_notation))
            
            return results
            
        except json.JSONDecodeError as e:
            raise ConversionError(f"Invalid response from batch conversion: {e}")
        except subprocess.TimeoutExpired:
            raise ConversionError(f"Batch conversion timed out for {len(rgb_colors)} colors")
        except Exception as e:
            raise ConversionError(f"Unexpected batch conversion error: {e}")
    
    def _validate_rgb(self, rgb: List[int]) -> None:
        """
        Validate RGB color values.
        
        Args:
            rgb (List[int]): RGB color as [R, G, B]
            
        Raises:
            ConversionError: If RGB values are invalid
        """
        if not isinstance(rgb, (list, tuple)) or len(rgb) != 3:
            raise ConversionError("RGB must be a list or tuple of exactly 3 values")
        
        for i, component in enumerate(rgb):
            if not isinstance(component, int):
                raise ConversionError(f"RGB component {i} must be an integer, got {type(component)}")
            if not 0 <= component <= 255:
                raise ConversionError(f"RGB component {i} must be in range 0-255, got {component}")
    
    def get_version(self) -> str:
        """
        Get the version of the underlying Rust library.
        
        Returns:
            str: Version string of the Rust MunsellSpace library
            
        Raises:
            ConversionError: If version cannot be determined
        """
        try:
            result = subprocess.run(
                [str(self._binary_path), "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                raise ConversionError(f"Failed to get version: {result.stderr}")
            
            return result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            raise ConversionError("Version check timed out")
        except Exception as e:
            raise ConversionError(f"Unexpected error getting version: {e}")
    
    def validate_reference_accuracy(self) -> dict:
        """
        Validate the converter against the reference dataset.
        
        This method runs the converter against the complete 4,007-color reference
        dataset and returns accuracy statistics.
        
        Returns:
            dict: Dictionary containing accuracy statistics:
                - total_colors: Total number of colors tested
                - exact_matches: Number of exact matches
                - accuracy_percentage: Percentage of exact matches
                - close_matches: Number of close matches (if applicable)
                
        Raises:
            ConversionError: If validation fails
            
        Note:
            This method may take several seconds to complete as it processes
            the entire reference dataset.
        """
        try:
            result = subprocess.run(
                [str(self._binary_path), "--validate"],
                capture_output=True,
                text=True,
                timeout=60  # Allow up to 1 minute for full validation
            )
            
            if result.returncode != 0:
                raise ConversionError(f"Validation failed: {result.stderr}")
            
            # Parse validation results
            output = json.loads(result.stdout)
            return output
            
        except json.JSONDecodeError as e:
            raise ConversionError(f"Invalid validation response: {e}")
        except subprocess.TimeoutExpired:
            raise ConversionError("Reference validation timed out")
        except Exception as e:
            raise ConversionError(f"Unexpected validation error: {e}")