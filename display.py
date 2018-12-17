import argparse
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument('gt', help='Path to GT MRI segment')
ap.add_argument('pred', nargs='+', help='Path to predicted MRI segment(s)')
ap.add_argument('modelnames', nargs='+', help='Display strings for MRI segment(s)')
args = ap.parse_args()

assert len(args.modelnames) == len(args.pred)

pred = []
for pfile in args.pred:
    pr = np.load(pfile)
    pred.append({pfile.split('.npy')[0].split('/')[-1]: pr})

gt = nib.load(args.gt).get_fdata()
flair = nib.load(args.gt.split('seg.nii.gz')[0]+'flair.nii.gz').get_fdata()

for idx in range(gt.shape[2]):
    
    pred_imgs = []
    for pred_dict in pred:
        pname = pred_dict.keys()[0]        
        pred_img = pred_dict[pname][:,:,idx]
        pred_imgs.append(pred_img)

    gt_img = gt[:,:,idx]
    flair_img = flair[:,:,idx]
    
    if np.sum(gt_img)>100:
        fig, ax = plt.subplots(nrows=1, ncols=len(pred_dict)+2)
        
        for idx in range(len(ax)):
            ax[idx].imshow(flair_img, cmap='gray')
        
        ax[0].text(0.5,-0.1, "Input MRI Slice", size=12, ha="center", transform=ax[0].transAxes)
        ax[1].imshow(gt_img, cmap='YlOrRd', alpha=.5)
        ax[1].text(0.5,-0.1, "GT Segmentation", size=12, ha="center", transform=ax[1].transAxes)
        
        for idx, (pred_name, pred_img) in enumerate(zip(args.modelnames, pred_imgs)):
            ax[2+idx].imshow(pred_img, cmap='YlOrRd', alpha=.5)
            ax[2+idx].text(0.5, -0.1, pred_name, size=12, ha="center", transform=ax[2+idx].transAxes)

        for axis in ax:
            axis.axis('off')
        
        plt.show()
