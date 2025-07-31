#!/usr/bin/env Rscript
# Test R aqp library col2Munsell function on ALL 4007 colors
# Complete dataset testing - no shortcuts

# Load required libraries
library(aqp)

# Function to load reference data
load_reference_data <- function(filepath) {
  # Read CSV file
  data <- read.csv(filepath, header = TRUE, stringsAsFactors = FALSE)
  
  # Return as data frame with proper column names
  colnames(data) <- c("R", "G", "B", "Expected_Munsell")
  return(data)
}

# Function to convert RGB to Munsell using aqp
rgb_to_munsell_aqp <- function(r, g, b) {
  tryCatch({
    # Convert RGB (0-255) to normalized (0-1) and create matrix
    rgb_matrix <- matrix(c(r/255, g/255, b/255), nrow = 1, ncol = 3)
    
    # Use col2Munsell from aqp package with sRGB space
    result <- col2Munsell(rgb_matrix, space = 'sRGB')
    
    # Extract the Munsell notation from the result
    if (is.null(result) || nrow(result) == 0) {
      return("ERROR: NULL result")
    }
    
    # Build Munsell notation string from hue, value, chroma
    hue <- result$hue[1]
    value <- result$value[1]
    chroma <- result$chroma[1]
    
    if (is.na(hue) || is.na(value) || is.na(chroma)) {
      return("ERROR: NA components")
    }
    
    # Format as Munsell notation (hue value/chroma)
    munsell_notation <- paste0(hue, " ", value, "/", chroma)
    return(munsell_notation)
    
  }, error = function(e) {
    return(paste("ERROR:", substr(as.character(e), 1, 50)))
  })
}

# Function to check if two Munsell notations are close matches
is_close_match <- function(result, expected) {
  if (grepl("ERROR", result)) {
    return(FALSE)
  }
  
  tryCatch({
    # Simple close match logic - could be more sophisticated
    # For now, check if they start with the same hue family
    result_clean <- gsub("\\s+", "", result)
    expected_clean <- gsub("\\s+", "", expected)
    
    # Extract hue family (letters at the end)
    result_family <- gsub(".*([A-Z]+)$", "\\1", result_clean)
    expected_family <- gsub(".*([A-Z]+)$", "\\1", expected_clean)
    
    return(result_family == expected_family)
  }, error = function(e) {
    return(FALSE)
  })
}

# Main test function
main <- function() {
  cat("R AQP LIBRARY TESTING - ALL 4007 COLORS\n")
  cat("Testing aqp::col2Munsell function on complete dataset\n")
  cat("=" , rep("=", 60), "\n", sep="")
  
  # Load reference data
  cat("Loading reference data...\n")
  reference_data <- load_reference_data("tests/data/srgb-to-munsell.csv")
  total_colors <- nrow(reference_data)
  
  cat("Loaded", total_colors, "reference colors\n")
  
  if (total_colors != 4007) {
    cat("WARNING: Expected 4007 colors, got", total_colors, "\n")
  }
  
  # Initialize counters
  exact_matches <- 0
  close_matches <- 0
  errors <- 0
  
  # Initialize example storage
  exact_examples <- character()
  error_examples <- character()
  miss_examples <- character()
  
  cat("Converting all colors using aqp::col2Munsell...\n")
  start_time <- Sys.time()
  
  # Process all colors
  for (i in 1:total_colors) {
    if (i %% 1000 == 0) {
      cat("  Processed", i, "/", total_colors, "colors...\n")
    }
    
    r <- reference_data$R[i]
    g <- reference_data$G[i]
    b <- reference_data$B[i]
    expected <- reference_data$Expected_Munsell[i]
    
    # Convert using aqp
    result <- rgb_to_munsell_aqp(r, g, b)
    
    # Check accuracy
    is_exact <- (result == expected)
    is_error <- grepl("ERROR", result)
    is_close <- if (!is_error && !is_exact) is_close_match(result, expected) else FALSE
    
    if (is_exact) {
      exact_matches <- exact_matches + 1
      if (length(exact_examples) < 10) {
        exact_examples <- c(exact_examples, 
                          sprintf("RGB(%3d,%3d,%3d) -> %s", r, g, b, result))
      }
    } else if (is_error) {
      errors <- errors + 1
      if (length(error_examples) < 10) {
        error_examples <- c(error_examples,
                          sprintf("RGB(%3d,%3d,%3d) -> %s", r, g, b, result))
      }
    } else if (is_close) {
      close_matches <- close_matches + 1
    } else {
      if (length(miss_examples) < 10) {
        miss_examples <- c(miss_examples,
                         sprintf("RGB(%3d,%3d,%3d) -> %s (expected: %s)", 
                                r, g, b, result, expected))
      }
    }
  }
  
  end_time <- Sys.time()
  processing_time <- as.numeric(difftime(end_time, start_time, units = "secs"))
  
  # Calculate statistics
  accuracy <- (exact_matches / total_colors) * 100
  error_rate <- (errors / total_colors) * 100
  close_match_rate <- (close_matches / total_colors) * 100
  combined_accuracy <- ((exact_matches + close_matches) / total_colors) * 100
  
  # Print comprehensive results
  cat("\n", rep("=", 60), "\n", sep="")
  cat("COMPLETE DATASET RESULTS - ALL 4007 COLORS - R AQP\n")
  cat(rep("=", 60), "\n", sep="")
  cat("Total colors tested:", total_colors, "\n")
  cat("Exact matches:", exact_matches, "\n")
  cat("Close matches:", close_matches, "\n")
  cat("Errors:", errors, "\n")
  cat("Complete misses:", total_colors - exact_matches - close_matches - errors, "\n")
  cat("\n")
  cat("ACCURACY METRICS:\n")
  cat("  Exact accuracy:", sprintf("%.3f%%", accuracy), "\n")
  cat("  Close match rate:", sprintf("%.3f%%", close_match_rate), "\n")
  cat("  Combined accuracy:", sprintf("%.3f%%", combined_accuracy), "\n")
  cat("  Error rate:", sprintf("%.3f%%", error_rate), "\n")
  cat("  Processing time:", sprintf("%.1f", processing_time), "seconds\n")
  
  # Show examples
  cat("\nEXACT MATCH EXAMPLES:\n")
  for (example in exact_examples[1:min(5, length(exact_examples))]) {
    cat(" ", example, "\n")
  }
  
  cat("\nERROR EXAMPLES:\n")
  for (example in error_examples[1:min(3, length(error_examples))]) {
    cat(" ", example, "\n")
  }
  
  cat("\nMISS EXAMPLES (not exact, not close):\n")
  for (example in miss_examples[1:min(3, length(miss_examples))]) {
    cat(" ", example, "\n")
  }
  
  # Save results summary
  filename <- sprintf("r_aqp_complete_results_%.1fpct.txt", accuracy)
  sink(filename)
  cat("COMPLETE 4007-COLOR DATASET RESULTS - R AQP\n")
  cat(rep("=", 50), "\n", sep="")
  cat("Total colors:", total_colors, "\n")
  cat("Exact matches:", exact_matches, "\n")
  cat("Close matches:", close_matches, "\n")
  cat("Errors:", errors, "\n")
  cat("Exact accuracy:", sprintf("%.3f%%", accuracy), "\n")
  cat("Combined accuracy:", sprintf("%.3f%%", combined_accuracy), "\n")
  cat("Processing time:", sprintf("%.1f", processing_time), "seconds\n")
  sink()
  
  cat("\nResults summary saved to:", filename, "\n")
  
  # Final assessment
  cat("\n", rep("=", 60), "\n", sep="")
  cat("R AQP LIBRARY ASSESSMENT\n")
  cat(rep("=", 60), "\n", sep="")
  
  if (accuracy >= 80.0) {
    status <- "EXCELLENT"
    cat("🎯", status, ": >80% exact accuracy - Strong reference implementation\n")
  } else if (accuracy >= 60.0) {
    status <- "GOOD"
    cat("✅", status, ": >60% exact accuracy - Good reference implementation\n")
  } else if (accuracy >= 40.0) {
    status <- "MODERATE"
    cat("⚠️", status, ": >40% exact accuracy - Moderate performance\n")
  } else if (accuracy >= 20.0) {
    status <- "POOR"
    cat("❌", status, ": >20% exact accuracy - Poor performance\n")
  } else {
    status <- "VERY POOR"
    cat("❌", status, ": <20% exact accuracy - Very poor performance\n")
  }
  
  cat("\nThis validates whether R aqp is suitable as reference implementation\n")
  cat("Target for Rust implementation:", sprintf("%.1f%%", accuracy), "exact accuracy\n")
  
  # Return results for comparison
  return(list(
    accuracy = accuracy,
    combined_accuracy = combined_accuracy,
    exact_matches = exact_matches,
    close_matches = close_matches,
    errors = errors,
    total = total_colors,
    processing_time = processing_time
  ))
}

# Run the main function
if (!interactive()) {
  results <- main()
}