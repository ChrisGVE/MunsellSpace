//! Criterion-based benchmarks for MunsellSpace conversion performance.

use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};
use munsellspace::MunsellConverter;
use std::hint::black_box as std_black_box;

/// Benchmark single color conversion performance
fn bench_single_conversion(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("single_conversion");
    
    // Different types of colors that exercise different code paths
    let test_cases = vec![
        ([255, 0, 0], "pure_red"),
        ([0, 255, 0], "pure_green"),
        ([0, 0, 255], "pure_blue"),
        ([128, 128, 128], "neutral_gray"),
        ([255, 255, 255], "pure_white"),
        ([0, 0, 0], "pure_black"),
        ([238, 0, 85], "convergence_case"),
        ([128, 64, 192], "random_color"),
        ([255, 128, 0], "orange"),
        ([64, 192, 128], "teal"),
    ];
    
    for (rgb, name) in test_cases {
        group.bench_with_input(
            BenchmarkId::new("srgb_to_munsell", name),
            &rgb,
            |b, &rgb| {
                b.iter(|| {
                    let result = converter.srgb_to_munsell(black_box(rgb))
                        .expect("Conversion failed");
                    std_black_box(result);
                });
            },
        );
    }
    
    group.finish();
}

/// Benchmark batch conversion performance with different batch sizes
fn bench_batch_conversion(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("batch_conversion");
    group.sample_size(20); // Reduce sample size for longer-running benchmarks
    
    // Generate test batches of different sizes
    let batch_sizes = vec![10, 50, 100, 500, 1000];
    
    for size in batch_sizes {
        let mut batch = Vec::with_capacity(size);
        for i in 0..size {
            let r = (i % 256) as u8;
            let g = ((i * 7) % 256) as u8; 
            let b = ((i * 13) % 256) as u8;
            batch.push([r, g, b]);
        }
        
        group.bench_with_input(
            BenchmarkId::new("convert_batch", size),
            &batch,
            |b, batch| {
                b.iter(|| {
                    let results = converter.convert_batch(black_box(batch))
                        .expect("Batch conversion failed");
                    std_black_box(results);
                });
            },
        );
    }
    
    group.finish();
}

/// Benchmark converter initialization performance
fn bench_converter_initialization(c: &mut Criterion) {
    c.bench_function("converter_initialization", |b| {
        b.iter(|| {
            let converter = MunsellConverter::new()
                .expect("Failed to create converter");
            std_black_box(converter);
        });
    });
}

/// Benchmark different color types to identify performance characteristics
fn bench_color_types(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("color_types");
    
    // High chroma colors (likely require more computation)
    let high_chroma_colors: Vec<[u8; 3]> = vec![
        [255, 0, 0], [0, 255, 0], [0, 0, 255],
        [255, 255, 0], [255, 0, 255], [0, 255, 255],
    ];
    
    group.bench_function("high_chroma", |b| {
        b.iter(|| {
            for &rgb in &high_chroma_colors {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("High chroma conversion failed");
                std_black_box(result);
            }
        });
    });
    
    // Low chroma colors (near neutral)
    let low_chroma_colors: Vec<[u8; 3]> = vec![
        [130, 128, 128], [128, 130, 128], [128, 128, 130],
        [140, 120, 120], [120, 140, 120], [120, 120, 140],
    ];
    
    group.bench_function("low_chroma", |b| {
        b.iter(|| {
            for &rgb in &low_chroma_colors {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("Low chroma conversion failed");
                std_black_box(result);
            }
        });
    });
    
    // Neutral colors (achromatic)
    let neutral_colors: Vec<[u8; 3]> = vec![
        [0, 0, 0], [64, 64, 64], [128, 128, 128],
        [192, 192, 192], [255, 255, 255],
    ];
    
    group.bench_function("neutral", |b| {
        b.iter(|| {
            for &rgb in &neutral_colors {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("Neutral conversion failed");
                std_black_box(result);
            }
        });
    });
    
    group.finish();
}

/// Benchmark edge cases and boundary colors
fn bench_edge_cases(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("edge_cases");
    
    // Colors at gamut boundaries
    let boundary_colors: Vec<[u8; 3]> = vec![
        [255, 1, 1], [1, 255, 1], [1, 1, 255],
        [255, 255, 1], [255, 1, 255], [1, 255, 255],
        [238, 0, 85], // Known convergence case
    ];
    
    group.bench_function("gamut_boundaries", |b| {
        b.iter(|| {
            for &rgb in &boundary_colors {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("Boundary color conversion failed");
                std_black_box(result);
            }
        });
    });
    
    // ISCC-NBS critical transition points
    let critical_points: Vec<[u8; 3]> = vec![
        [85, 17, 238],   // Critical value=3.5
        [68, 34, 153],   // Critical value=2.5
        [0, 34, 85],     // Critical chroma=7.0
        [17, 51, 136],   // Critical chroma=11.0
        [51, 34, 153],   // Critical chroma=15.0
    ];
    
    group.bench_function("iscc_critical", |b| {
        b.iter(|| {
            for &rgb in &critical_points {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("Critical point conversion failed");
                std_black_box(result);
            }
        });
    });
    
    group.finish();
}

/// Benchmark memory usage patterns with large datasets
fn bench_memory_patterns(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("memory_patterns");
    group.sample_size(10);
    
    // Large batch - tests memory allocation patterns
    let large_batch: Vec<[u8; 3]> = (0..5000)
        .map(|i| [
            (i % 256) as u8,
            ((i / 256) % 256) as u8,
            ((i / 65536) % 256) as u8,
        ])
        .collect();
    
    group.bench_function("large_batch_5000", |b| {
        b.iter(|| {
            let results = converter.convert_batch(black_box(&large_batch))
                .expect("Large batch conversion failed");
            std_black_box(results);
        });
    });
    
    // Sequential individual conversions vs batch
    group.bench_function("sequential_5000", |b| {
        b.iter(|| {
            let mut results = Vec::with_capacity(large_batch.len());
            for &rgb in &large_batch {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("Sequential conversion failed");
                results.push(result);
            }
            std_black_box(results);
        });
    });
    
    group.finish();
}

/// Benchmark realistic workloads
fn bench_realistic_workloads(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("realistic_workloads");
    group.sample_size(30);
    
    // Image processing workload - mixed colors
    let image_colors: Vec<[u8; 3]> = vec![
        // Skin tones
        [255, 219, 172], [241, 194, 125], [224, 172, 105], [198, 134, 66],
        [141, 85, 36], [255, 206, 84], [233, 176, 122], [210, 180, 140],
        
        // Sky and water
        [135, 206, 235], [70, 130, 180], [100, 149, 237], [30, 144, 255],
        [0, 191, 255], [65, 105, 225], [72, 61, 139], [25, 25, 112],
        
        // Vegetation
        [34, 139, 34], [0, 128, 0], [0, 100, 0], [85, 107, 47],
        [124, 252, 0], [127, 255, 0], [50, 205, 50], [152, 251, 152],
        
        // Common objects
        [255, 0, 0], [255, 165, 0], [255, 255, 0], [128, 0, 128],
        [255, 192, 203], [165, 42, 42], [128, 128, 128], [0, 0, 0],
    ];
    
    group.bench_function("image_processing", |b| {
        b.iter(|| {
            for &rgb in &image_colors {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("Image color conversion failed");
                std_black_box(result);
            }
        });
    });
    
    // Color palette generation workload
    let palette_size = 50;
    let palette_colors: Vec<[u8; 3]> = (0..palette_size)
        .map(|i| {
            let hue = (i * 360 / palette_size) as f32;
            let saturation = 0.8;
            let value = 0.9;
            
            // Convert HSV to RGB
            let c = value * saturation;
            let x = c * (1.0 - ((hue / 60.0) % 2.0 - 1.0).abs());
            let m = value - c;
            
            let (r, g, b) = if hue < 60.0 {
                (c, x, 0.0)
            } else if hue < 120.0 {
                (x, c, 0.0)
            } else if hue < 180.0 {
                (0.0, c, x)
            } else if hue < 240.0 {
                (0.0, x, c)
            } else if hue < 300.0 {
                (x, 0.0, c)
            } else {
                (c, 0.0, x)
            };
            
            [
                ((r + m) * 255.0) as u8,
                ((g + m) * 255.0) as u8,
                ((b + m) * 255.0) as u8,
            ]
        })
        .collect();
    
    group.bench_function("palette_generation", |b| {
        b.iter(|| {
            for &rgb in &palette_colors {
                let result = converter.srgb_to_munsell(black_box(rgb))
                    .expect("Palette color conversion failed");
                std_black_box(result);
            }
        });
    });
    
    group.finish();
}

criterion_group!(
    benches,
    bench_single_conversion,
    bench_batch_conversion,
    bench_converter_initialization,
    bench_color_types,
    bench_edge_cases,
    bench_memory_patterns,
    bench_realistic_workloads
);
criterion_main!(benches);