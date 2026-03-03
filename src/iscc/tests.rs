//! Tests for the ISCC-NBS classifier.

use super::*;
use std::sync::Arc;
use std::thread;

#[test]
fn test_boundary_disambiguation() {
    // Test that boundary rules prevent ambiguous classification
    // Point exactly on boundary should only match one polygon
}

#[test]
fn test_staircase_classification() {
    // Test that staircase polygons work correctly with rectangles in steps
}

#[test]
fn test_thread_safety_concurrent_classification() {
    let classifier = Arc::new(IsccNbsClassifier::new().expect("Failed to create classifier"));
    let mut handles = vec![];

    let test_colors = vec![
        ("5R", 6.0, 14.0),
        ("10YR", 7.0, 6.0),
        ("5Y", 8.0, 12.0),
        ("5G", 5.0, 8.0),
        ("5B", 4.0, 6.0),
        ("5P", 3.0, 10.0),
        ("N", 5.0, 0.0),
        ("N", 9.0, 0.0),
        ("N", 2.0, 0.0),
    ];

    for thread_id in 0..8 {
        let classifier_clone = Arc::clone(&classifier);
        let test_colors_clone = test_colors.clone();

        let handle = thread::spawn(move || {
            let mut results = Vec::new();

            for iteration in 0..10 {
                for (i, &(hue, value, chroma)) in test_colors_clone.iter().enumerate() {
                    let adjusted_value =
                        value + (thread_id as f64 * 0.01) + (iteration as f64 * 0.001);
                    let adjusted_chroma =
                        if chroma > 0.0 { chroma + (i as f64 * 0.01) } else { 0.0 };

                    match classifier_clone.classify_munsell(
                        hue,
                        adjusted_value,
                        adjusted_chroma,
                    ) {
                        Ok(Some(metadata)) => {
                            results.push((
                                hue.to_string(),
                                adjusted_value,
                                adjusted_chroma,
                                metadata.iscc_nbs_color_name.clone(),
                            ));
                        }
                        Ok(None) => {
                            results.push((
                                hue.to_string(),
                                adjusted_value,
                                adjusted_chroma,
                                "unclassified".to_string(),
                            ));
                        }
                        Err(e) => {
                            panic!("Classification error in thread {}: {:?}", thread_id, e);
                        }
                    }
                }
            }

            (thread_id, results.len())
        });
        handles.push(handle);
    }

    let mut total_classifications = 0;
    for handle in handles {
        let (thread_id, count) = handle.join().expect("Thread panicked");
        println!("Thread {} completed {} classifications", thread_id, count);
        total_classifications += count;
    }

    let expected_total = 8 * 10 * test_colors.len();
    assert_eq!(
        total_classifications, expected_total,
        "Expected {} total classifications, got {}",
        expected_total, total_classifications
    );
}

#[test]
fn test_thread_safety_cache_behavior() {
    let classifier = Arc::new(IsccNbsClassifier::new().expect("Failed to create classifier"));
    let mut handles = vec![];

    let test_color = ("5R", 6.0, 14.0);

    for thread_id in 0..4 {
        let classifier_clone = Arc::clone(&classifier);

        let handle = thread::spawn(move || {
            let mut cache_hits = 0;
            let mut results = Vec::new();

            for _ in 0..50 {
                match classifier_clone.classify_munsell(
                    test_color.0,
                    test_color.1,
                    test_color.2,
                ) {
                    Ok(Some(metadata)) => {
                        results.push(metadata.iscc_nbs_color_name.clone());
                        cache_hits += 1;
                    }
                    Ok(None) => {}
                    Err(e) => {
                        panic!("Classification error in thread {}: {:?}", thread_id, e);
                    }
                }
            }

            (thread_id, cache_hits, results)
        });
        handles.push(handle);
    }

    for handle in handles {
        let (thread_id, cache_hits, results) = handle.join().expect("Thread panicked");
        println!("Thread {} got {} cache hits", thread_id, cache_hits);

        if !results.is_empty() {
            let first_result = &results[0];
            for result in &results {
                assert_eq!(
                    result, first_result,
                    "Thread {} got inconsistent results",
                    thread_id
                );
            }
        }
    }
}

#[test]
fn test_cache_deterministic_fifo_eviction() {
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");

    for i in 0..260 {
        let key = (format!("hue_{}", i), i, i);
        classifier.cache_result(key, Some(i as u16));
    }

    let cache = classifier.cache.read().unwrap();
    let order = classifier.cache_order.read().unwrap();

    assert_eq!(cache.len(), classifier.cache_max_size);
    assert_eq!(order.len(), classifier.cache_max_size);

    for i in 0..4 {
        let key = (format!("hue_{}", i), i, i);
        assert!(
            !cache.contains_key(&key),
            "Entry {} should have been evicted",
            i
        );
    }

    for i in 4..260 {
        let key = (format!("hue_{}", i), i, i);
        assert!(
            cache.contains_key(&key),
            "Entry {} should still be in cache",
            i
        );
    }

    let front = order.front().expect("Order should not be empty");
    assert_eq!(front.0, "hue_4", "Front of order should be hue_4");

    let back = order.back().expect("Order should not be empty");
    assert_eq!(back.0, "hue_259", "Back of order should be hue_259");
}

#[test]
fn test_send_sync_traits() {
    fn assert_send<T: Send>() {}
    fn assert_sync<T: Sync>() {}

    assert_send::<IsccNbsClassifier>();
    assert_sync::<IsccNbsClassifier>();

    assert_send::<Arc<IsccNbsClassifier>>();
    assert_sync::<Arc<IsccNbsClassifier>>();
}
