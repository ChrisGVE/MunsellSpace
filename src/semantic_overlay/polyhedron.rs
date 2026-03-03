//! Convex polyhedron point-in-polyhedron algorithm.

use super::types::{MunsellCartesian, MunsellSpec};

/// A triangular face of a polyhedron, defined by vertex indices.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct TriFace {
    /// Index of first vertex
    pub v0: usize,
    /// Index of second vertex
    pub v1: usize,
    /// Index of third vertex
    pub v2: usize,
}

impl TriFace {
    /// Create a new triangular face from vertex indices.
    pub fn new(v0: usize, v1: usize, v2: usize) -> Self {
        Self { v0, v1, v2 }
    }
}

/// Represents a convex polyhedron defined by vertices and triangular faces.
#[derive(Debug, Clone)]
pub struct ConvexPolyhedron {
    /// Vertices as 3D Cartesian coordinates
    pub vertices: Vec<MunsellCartesian>,
    /// Triangular faces as vertex indices (counter-clockwise when viewed from outside)
    pub faces: Vec<TriFace>,
}

impl ConvexPolyhedron {
    /// Create a new convex polyhedron.
    pub fn new(vertices: Vec<MunsellCartesian>, faces: Vec<TriFace>) -> Self {
        Self { vertices, faces }
    }

    /// Create from arrays of vertex coordinates and face indices.
    pub fn from_arrays(vertices: &[(f64, f64, f64)], faces: &[(usize, usize, usize)]) -> Self {
        let verts: Vec<MunsellCartesian> = vertices
            .iter()
            .map(|(x, y, z)| MunsellCartesian::new(*x, *y, *z))
            .collect();

        let face_list: Vec<TriFace> = faces
            .iter()
            .map(|(v0, v1, v2)| TriFace::new(*v0, *v1, *v2))
            .collect();

        Self::new(verts, face_list)
    }

    /// Calculate the centroid (geometric center) of the polyhedron.
    pub fn centroid(&self) -> MunsellCartesian {
        if self.vertices.is_empty() {
            return MunsellCartesian::new(0.0, 0.0, 0.0);
        }

        let n = self.vertices.len() as f64;
        let sum_x: f64 = self.vertices.iter().map(|v| v.x).sum();
        let sum_y: f64 = self.vertices.iter().map(|v| v.y).sum();
        let sum_z: f64 = self.vertices.iter().map(|v| v.z).sum();

        MunsellCartesian::new(sum_x / n, sum_y / n, sum_z / n)
    }

    /// Test if a point is inside this convex polyhedron.
    ///
    /// Uses the half-space test: for a convex polyhedron, a point is inside
    /// if and only if it is on the interior side of every face plane.
    pub fn contains_point(&self, point: &MunsellCartesian) -> bool {
        if self.faces.is_empty() || self.vertices.len() < 4 {
            return false;
        }

        let centroid = self.centroid();

        for face in &self.faces {
            let v0 = &self.vertices[face.v0];
            let v1 = &self.vertices[face.v1];
            let v2 = &self.vertices[face.v2];

            let edge1 = (v1.x - v0.x, v1.y - v0.y, v1.z - v0.z);
            let edge2 = (v2.x - v0.x, v2.y - v0.y, v2.z - v0.z);

            let normal = cross_product(edge1, edge2);
            let d = -(normal.0 * v0.x + normal.1 * v0.y + normal.2 * v0.z);

            let point_side =
                normal.0 * point.x + normal.1 * point.y + normal.2 * point.z + d;
            let centroid_side =
                normal.0 * centroid.x + normal.1 * centroid.y + normal.2 * centroid.z + d;

            const EPSILON: f64 = 1e-10;
            if centroid_side > EPSILON {
                if point_side < -EPSILON {
                    return false;
                }
            } else if centroid_side < -EPSILON {
                if point_side > EPSILON {
                    return false;
                }
            }
        }

        true
    }

    /// Test if a point is inside with a tolerance for near-boundary points.
    pub fn contains_point_with_tolerance(&self, point: &MunsellCartesian, tolerance: f64) -> bool {
        if self.contains_point(point) {
            return true;
        }

        // Check if point is within tolerance distance of any vertex
        for vertex in &self.vertices {
            if point.distance(vertex) <= tolerance {
                return true;
            }
        }

        false
    }
}

/// Calculate cross product of two 3D vectors.
fn cross_product(a: (f64, f64, f64), b: (f64, f64, f64)) -> (f64, f64, f64) {
    (
        a.1 * b.2 - a.2 * b.1,
        a.2 * b.0 - a.0 * b.2,
        a.0 * b.1 - a.1 * b.0,
    )
}

/// Test if a point is inside a convex polyhedron (standalone function).
pub fn point_in_polyhedron(
    point: &MunsellCartesian,
    vertices: &[(f64, f64, f64)],
    faces: &[(usize, usize, usize)],
) -> bool {
    let poly = ConvexPolyhedron::from_arrays(vertices, faces);
    poly.contains_point(point)
}

/// Test if a Munsell color is inside a polyhedron (convenience function).
pub fn munsell_in_polyhedron(
    color: &MunsellSpec,
    vertices: &[(f64, f64, f64)],
    faces: &[(usize, usize, usize)],
) -> bool {
    let point = color.to_cartesian();
    point_in_polyhedron(&point, vertices, faces)
}
