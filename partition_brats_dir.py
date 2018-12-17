import argparse
import os
import glob

def get_dataset_dirnames(direc, part='train'):
    
    files = glob.glob(os.path.join(direc, '*'))
    
    l = len(files)
    train_ptr = int(l*.8)
    val_ptr = int(train_ptr+l*.1)

    if part == 'train':
        return [fl.split('/')[-1] for fl in files[:train_ptr]]
    elif part == 'val':
        return [fl.split('/')[-1] for fl in files[train_ptr:val_ptr]]
    else:
        return [fl.split('/')[-1] for fl in files[val_ptr:]]

if __name__=='__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True, help='Directory of nii.gz files to split into train, val and test sets')
    args = ap.parse_args()
    
    for part in ['train', 'val', 'test']:
        fnames = get_dataset_dirnames(args.dir, part)

        with open(part+'.txt', 'w') as f:
            for fn in fnames:
                f.write(fn+'\n')
    
