//! Performance benchmarks for MunsellSpace library using Criterion.
//!
//! These benchmarks measure the performance of critical conversion functions
//! to ensure they meet performance requirements and detect regressions.

use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};
use munsellspace::{
    MunsellConverter,
    IsccNbsClassifier,
    mathematical::MathematicalMunsellConverter,
    reverse_conversion::ReverseConverter,
    MunsellColor
};
use std::sync::Arc;

/// Benchmark single RGB to Munsell conversions
fn bench_single_conversion(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("single_conversion");
    
    // Test different types of colors
    let test_colors = [
        ([255, 0, 0], "pure_red"),
        ([0, 255, 0], "pure_green"), 
        ([0, 0, 255], "pure_blue"),
        ([128, 128, 128], "middle_gray"),
        ([0, 0, 0], "black"),
        ([255, 255, 255], "white"),
        ([255, 165, 0], "orange"),
        ([139, 69, 19], "brown"),
        ([255, 192, 203], "pink"),
        ([128, 0, 128], "purple"),
    ];
    
    for (rgb, name) in &test_colors {
        group.bench_with_input(
            BenchmarkId::new("srgb_to_munsell", name),
            rgb,
            |b, &rgb| {
                b.iter(|| {
                    black_box(converter.srgb_to_munsell(black_box(rgb)))
                });
            }
        );
    }
    
    group.finish();
}

/// Benchmark batch conversion performance
fn bench_batch_conversion(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("batch_conversion");
    
    // Generate test batches of different sizes
    let batch_sizes = [10, 100, 1000];
    
    for &size in &batch_sizes {
        let batch: Vec<[u8; 3]> = (0..size)
            .map(|i| [
                ((i * 17) % 256) as u8,
                ((i * 37) % 256) as u8,
                ((i * 73) % 256) as u8,
            ])
            .collect();
        
        group.bench_with_input(
            BenchmarkId::new("convert_batch", size),
            &batch,
            |b, batch| {
                b.iter(|| {
                    black_box(converter.convert_batch(black_box(batch)))
                });
            }
        );
    }
    
    group.finish();
}

/// Benchmark mathematical converter performance
fn bench_mathematical_converter(c: &mut Criterion) {
    let converter = MathematicalMunsellConverter::new().expect("Failed to create mathematical converter");
    
    let mut group = c.benchmark_group("mathematical_conversion");
    
    let test_colors = [
        [255, 0, 0],     // Red
        [0, 255, 0],     // Green
        [0, 0, 255],     // Blue
        [128, 128, 128], // Gray
        [255, 255, 255], // White
    ];
    
    for (i, &rgb) in test_colors.iter().enumerate() {
        group.bench_with_input(
            BenchmarkId::new("srgb_to_xyy", i),
            &rgb,
            |b, &rgb| {
                b.iter(|| {
                    black_box(converter.srgb_to_xyy(black_box(rgb)))
                });
            }
        );
        
        // Also benchmark the full pipeline if conversion succeeds
        if let Ok(xyy) = converter.srgb_to_xyy(rgb) {
            group.bench_with_input(
                BenchmarkId::new("xyy_to_munsell", i),
                &xyy,
                |b, &xyy| {
                    b.iter(|| {
                        black_box(converter.xyy_to_munsell_specification(black_box(xyy)))
                    });
                }
            );
        }
    }
    
    group.finish();
}

/// Benchmark ISCC-NBS classification performance
fn bench_iscc_nbs_classification(c: &mut Criterion) {
    let classifier = IsccNbsClassifier::new().expect("Failed to create ISCC-NBS classifier");
    
    let mut group = c.benchmark_group("iscc_nbs_classification");
    
    let test_colors = [
        [255, 0, 0],     // Red
        [0, 255, 0],     // Green
        [0, 0, 255],     // Blue
        [255, 255, 0],   // Yellow
        [255, 0, 255],   // Magenta
        [0, 255, 255],   // Cyan
        [128, 128, 128], // Gray
        [139, 69, 19],   // Brown
        [255, 192, 203], // Pink
        [128, 0, 128],   // Purple
    ];
    
    for (i, &rgb) in test_colors.iter().enumerate() {
        group.bench_with_input(
            BenchmarkId::new("classify_srgb", i),
            &rgb,
            |b, &rgb| {
                b.iter(|| {
                    black_box(classifier.classify_srgb(black_box(rgb)))
                });
            }
        );
    }
    
    group.finish();
}

/// Benchmark reverse conversion performance (Munsell to RGB)
fn bench_reverse_conversion(c: &mut Criterion) {
    let reverse_converter = ReverseConverter::new().expect("Failed to create reverse converter");
    
    let mut group = c.benchmark_group("reverse_conversion");
    
    let test_munsell_notations = [
        "5R 4.0/14.0",
        "10YR 6.0/8.0",
        "5G 5.0/12.0",
        "5B 3.0/6.0",
        "N 5.0",
        "2.5RP 7.0/10.0",
        "7.5PB 4.0/8.0",
        "N 0.0",
        "N 9.0",
        "10R 8.0/2.0",
    ];
    
    for (i, &notation) in test_munsell_notations.iter().enumerate() {
        if let Ok(munsell_color) = MunsellColor::from_notation(notation) {
            group.bench_with_input(
                BenchmarkId::new("munsell_to_srgb", i),
                &munsell_color,
                |b, munsell_color| {
                    b.iter(|| {
                        black_box(reverse_converter.munsell_to_srgb(black_box(&munsell_color)))
                    });
                }
            );
        }
    }
    
    group.finish();
}

/// Benchmark thread safety by running conversions concurrently
fn bench_thread_safety(c: &mut Criterion) {
    let converter = Arc::new(MunsellConverter::new().expect("Failed to create converter"));
    
    let mut group = c.benchmark_group("thread_safety");
    
    let test_colors: Vec<[u8; 3]> = (0..100)
        .map(|i| [
            ((i * 17) % 256) as u8,
            ((i * 37) % 256) as u8,
            ((i * 73) % 256) as u8,
        ])
        .collect();
    
    group.bench_function("concurrent_conversions", |b| {
        b.iter(|| {
            use std::thread;
            
            let handles: Vec<_> = (0..4)
                .map(|thread_id| {
                    let converter_clone = Arc::clone(&converter);
                    let colors_subset = test_colors
                        .iter()
                        .skip(thread_id * 25)
                        .take(25)
                        .copied()
                        .collect::<Vec<_>>();
                    
                    thread::spawn(move || {
                        colors_subset.iter()
                            .map(|&rgb| converter_clone.srgb_to_munsell(rgb))
                            .collect::<Result<Vec<_>, _>>()
                    })
                })
                .collect();
            
            let results: Vec<_> = handles.into_iter()
                .map(|h| h.join().unwrap())
                .collect();
            
            black_box(results)
        });
    });
    
    group.finish();
}

/// Benchmark Munsell notation parsing performance
fn bench_notation_parsing(c: &mut Criterion) {
    let mut group = c.benchmark_group("notation_parsing");
    
    let test_notations = [
        "5R 4.0/14.0",
        "N 5.0",
        "2.5YR 6.5/8.5",
        "10BG 3.2/12.8",
        "7.5P 8.1/4.2",
        "N 0.0",
        "N 9.5",
        "0.5GY 4.7/11.3",
        "9.9RP 2.1/15.6",
        "5.0B 6.8/9.4",
    ];
    
    for (i, &notation) in test_notations.iter().enumerate() {
        group.bench_with_input(
            BenchmarkId::new("from_notation", i),
            notation,
            |b, notation| {
                b.iter(|| {
                    black_box(MunsellColor::from_notation(black_box(notation)))
                });
            }
        );
    }
    
    group.finish();
}

/// Benchmark reference dataset lookup performance
fn bench_reference_lookup(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("reference_lookup");
    
    // Use colors that are likely to be in the reference dataset
    let reference_colors = [
        [255, 0, 0],   // Pure red - likely in dataset
        [0, 255, 0],   // Pure green - likely in dataset
        [0, 0, 255],   // Pure blue - likely in dataset
        [0, 0, 0],     // Black - definitely in dataset
        [255, 255, 255], // White - likely in dataset
    ];
    
    for (i, &rgb) in reference_colors.iter().enumerate() {
        group.bench_with_input(
            BenchmarkId::new("reference_lookup", i),
            &rgb,
            |b, &rgb| {
                b.iter(|| {
                    // This will test both lookup and fallback to mathematical conversion
                    black_box(converter.srgb_to_munsell(black_box(rgb)))
                });
            }
        );
    }
    
    group.finish();
}

/// Comprehensive benchmark measuring memory allocation patterns
fn bench_memory_usage(c: &mut Criterion) {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let mut group = c.benchmark_group("memory_usage");
    
    // Benchmark repeated conversions to test memory allocation patterns
    group.bench_function("repeated_conversions", |b| {
        let colors: Vec<[u8; 3]> = (0..1000)
            .map(|i| [
                ((i * 17) % 256) as u8,
                ((i * 37) % 256) as u8,
                ((i * 73) % 256) as u8,
            ])
            .collect();
        
        b.iter(|| {
            for &rgb in &colors {
                black_box(converter.srgb_to_munsell(black_box(rgb)).unwrap());
            }
        });
    });
    
    group.finish();
}

criterion_group!(
    benches,
    bench_single_conversion,
    bench_batch_conversion,
    bench_mathematical_converter,
    bench_iscc_nbs_classification,
    bench_reverse_conversion,
    bench_thread_safety,
    bench_notation_parsing,
    bench_reference_lookup,
    bench_memory_usage
);
criterion_main!(benches);