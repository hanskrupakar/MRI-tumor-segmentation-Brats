import argparse
import os
import glob

if __name__=='__main__':
	
	ap = argparse.ArgumentParser()
	ap.add_argument('--dir', required=True, help='Directory of nii.gz files to split into train, val and test sets')
	args = ap.parse_args()
	
	files = glob.glob(os.path.join(args.dir, '*'))
	
	l = len(files)
	train_ptr = int(l*.8)
	val_ptr = int(train_ptr+l*.1)
	
	with open('train.txt', 'w') as f:
		for fl in files[:train_ptr]:
			f.write(fl.split('/')[-1]+'\n')	    	
	with open('val.txt', 'w') as f:
		for fl in files[train_ptr:val_ptr]:
			f.write(fl.split('/')[-1]+'\n')	    	
	with open('test.txt', 'w') as f:
		for fl in files[val_ptr:]:
			f.write(fl.split('/')[-1]+'\n')	    	
		
