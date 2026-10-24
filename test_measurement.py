import unittest
from measurement import analyze, synthetic_fixture
class MeasurementTests(unittest.TestCase):
 def test_known_effect_and_common_trend(self):
  r=analyze(synthetic_fixture());self.assertEqual(r['mean_change_contrast'],9);self.assertEqual(r['naive_treated_change'],29);self.assertEqual(r['mean_control_change'],20)
 def test_exact_enumeration(self):
  rows=[dict(pair=i,treated_pre=100,treated_post=110,control_pre=100,control_post=100) for i in range(4)]
  self.assertEqual(analyze(rows)['exact_two_sided_p'],2/16)
 def test_zero_change_null(self):
  rows=[dict(pair=i,treated_pre=100,treated_post=120,control_pre=100,control_post=120) for i in range(4)]
  self.assertEqual(analyze(rows)['exact_two_sided_p'],1)
 def test_common_shock_invariance(self):
  a=synthetic_fixture();b=[dict(r,treated_post=r['treated_post']+100,control_post=r['control_post']+100) for r in a]
  self.assertEqual(analyze(a)['mean_change_contrast'],analyze(b)['mean_change_contrast'])
 def test_label_swap(self):
  a=synthetic_fixture();b=[dict(pair=r['pair'],treated_pre=r['control_pre'],treated_post=r['control_post'],control_pre=r['treated_pre'],control_post=r['treated_post']) for r in a]
  self.assertEqual(analyze(a)['mean_change_contrast'],-analyze(b)['mean_change_contrast']);self.assertEqual(analyze(a)['exact_two_sided_p'],analyze(b)['exact_two_sided_p'])
 def test_duplicate_rejected(self):
  a=synthetic_fixture();a[1]['pair']=a[0]['pair']
  with self.assertRaises(ValueError):analyze(a)
 def test_nonfinite_rejected(self):
  a=synthetic_fixture();a[0]['control_post']=float('nan')
  with self.assertRaises(ValueError):analyze(a)
if __name__=='__main__':unittest.main()
