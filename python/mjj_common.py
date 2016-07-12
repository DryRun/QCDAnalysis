import array

# Rebin a histogram according to approximate mass resolution. 
def apply_dijet_binning(hist, bins=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8000]):
	bins = array.array('d', bins)
	rebinned_hist = hist.Rebin(len(bins) - 1, hist.GetName() + "_rebinned", bins)
	return rebinned_hist

def apply_dijet_binning_normalized(hist, bins=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8000], bin_width = 1.):
	rebinned_hist = apply_dijet_binning(hist, bins)
	for bin in xrange(1, rebinned_hist.GetNbinsX() + 1):
		rebinned_hist.SetBinContent(bin, rebinned_hist.GetBinContent(bin) / rebinned_hist.GetXaxis().GetBinWidth(bin) * bin_width)
		rebinned_hist.SetBinError(bin, rebinned_hist.GetBinError(bin) / rebinned_hist.GetXaxis().GetBinWidth(bin) * bin_width)
	return rebinned_hist

# Blind a histogram between [center - half_width, center + half_width]
def blind_histogram(hist, center=750., half_width=75.):
	hist_blind = hist.Clone()
	for bin in xrange(1, hist_blind.GetNbinsX() + 1):
		if TMath.Abs(hist_blind.GetBinCenter(bin) - center) < half_width:
			hist_blind.SetBinContent(bin, 0.)
			hist_blind.SetBinError(bin, 0.)
	return hist_blind
