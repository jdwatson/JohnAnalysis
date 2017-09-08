#This script returns a transfer function when passed two 1D arrays of the x and y values.
#Different functions can be used for performing different types of fits
import numpy as np
import peakutils


'''Generate transfer function from SET response vs SET gate and AWG ramp.  Function requires as input the start and 
end points of transfer function and then performs a polynomial fit to the data'''
def AWG_Transfer(VgSET, SET_response, transfer_start, transfer_end, deg = 5, NPoints = 1000):

    xtransfer_fit = np.linspace(VgSET[0], VgSET[len(VgSET)], NPoints)
    g_transfer_fit = np.polyval(np.polyfit(VgSET, SET_response, deg), xtransfer_fit)

    return xtransfer_fit, g_transfer_fit



def Luca(x, g_set):
    """1) Find peaks 2) Find valleys 3) Extract curve from peak to valley 4) Polynomial fit"""

    # 1) Peaks
    peak_idx = peakutils.indexes(g_set, thres=0.5, min_dist=30)
    if np.size(peak_idx) == 0:
        raise ValueError("No peak detected")
    peak_position = x[peak_idx]
    peaks = g_set[peak_idx]

    #period = np.sum(peak_position) / np.size(peak_position)
    period = (peak_position[-1] - peak_position[0]) / np.size(peak_position)

    # 2) Valleys
    try:
        baseline = peakutils.baseline(g_set, deg=5, max_it=100, tol=0.0001)
        loc_min_idx = np.where(np.diff(np.sign(g_set - baseline)) > 0)
        plt.plot(x, baseline)
        print("baseline function worked")
    except:
        loc_min_idx = sig.argrelmin(g_set, order=2)
        print("relative min function worked")

    if np.size(loc_min_idx) == 0:
        raise ValueError("No minima detected")

    loc_min_pos = x[loc_min_idx]
    loc_min = g_set[loc_min_idx]

    plt.plot(x, g_set)
    plt.scatter(peak_position, peaks)
    plt.scatter(loc_min_pos, loc_min)
    plt.show()

    # 3) Transfer function
    if peak_idx[0] < loc_min_idx[0][0]:
        choose_peak = peak_idx[1] #peak_idx[2]
        choose_valley = loc_min_idx[0][2]
    else:
        choose_peak = peak_idx[0]
        choose_valley = loc_min_idx[0][1]

    mid_idx = int((choose_peak + choose_valley) / 2)
    mid_pos = x[mid_idx]  # Vg operating point

    print("Chosen peak voltage:", x[choose_peak], "Chosen valley voltage:", x[choose_valley], "Chosen OP voltage:",
          mid_pos)

    #x = x / period

    distance = int((choose_valley - choose_peak) / 2)
    xtransfer = x[mid_idx - distance:mid_idx + distance]
    g_transfer = g_set[mid_idx - distance:mid_idx + distance]

    # 4) Fit
    xtransfer_fit = np.linspace(x[mid_idx - distance], x[mid_idx + distance], 10 * (np.size(xtransfer) - 1) + 1)
    g_transfer_fit = np.polyval(np.polyfit(xtransfer, g_transfer, 4), xtransfer_fit)

    plt.plot(xtransfer_fit, g_transfer_fit)
    plt.plot(xtransfer, g_transfer)
    plt.show()

    fit_error = 0
    for i in range(np.size(xtransfer)):
        fit_error += (g_transfer[i] - g_transfer_fit[i * 10]) / g_transfer[i]

    # print("mean fit error:", fit_error)

    fit_error = fit_error / np.size(xtransfer)
    # print("mean fit error:", fit_error)

    if fit_error > 0.1:
        raise ValueError("Error during fit")
    print("mean fit error:", fit_error)

    return period, mid_pos, xtransfer_fit, g_transfer_fit
