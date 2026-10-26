import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from causalforge.ingest import incident_from_dict


class IngestValidationTests(unittest.TestCase):
    def test_nan_timestamp_names_the_node(self):
        with self.assertRaises(ValueError) as ctx:
            incident_from_dict({"nodes": [{"id": "n1", "t_start": "NaN"}]})
        self.assertIn("n1", str(ctx.exception))

    def test_infinite_coupling_names_the_edge(self):
        with self.assertRaises(ValueError) as ctx:
            incident_from_dict({"nodes": [{"id": "a"}, {"id": "b"}],
                                "edges": [{"src": "a", "dst": "b", "coupling": "Infinity"}]})
        self.assertIn("a->b", str(ctx.exception))

    def test_valid_incident_parses(self):
        inc = incident_from_dict({"nodes": [{"id": "a", "t_start": 1.0}],
                                  "edges": [{"src": "a", "dst": "a", "coupling": 0.5}]})
        self.assertEqual(inc.nodes[0].t_start, 1.0)
        self.assertEqual(inc.edges[0].coupling, 0.5)


if __name__ == "__main__":
    unittest.main()
