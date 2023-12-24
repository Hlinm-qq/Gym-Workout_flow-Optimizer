import pandas as pd
import numpy as np

def getEquipments(filePath):
    df = pd.read_csv(filePath)['equipment'].values
    return df

# print(getEquipments('data\equipment_list.csv'))
['treadmill' 'rowing machine' 'upright bike' 'elliptical machine' 'bench'
 'squat machine' 'leg press and hack squat machine' 'standing calf'     
 'abdominal machine' 'spin machine' 'biceps curl' 'rear delt/pec fly'   
 'multi press machine' 'inner/outer thigh' 'leg press/calf extension'   
 'lying leg curl' 'pulldown/seated row' 'functional trainer'
 'olympic bench' 'preacher curl slate' 'leg extension' 'leg curl'       
 'rotary torso' 'triceps extension' 'lateral raise' 'lat pulldown'      
 'shoulder press' 'booty builder 7' 'multi-purpose squat rack'
 'large dumbbell rack' 'vertical dumbbell rack'
 'free standing space saving modular rig'
 'precor multu gym s3.45-upper body' 'precor multu gym s3.45-lower body' 'precor multu gym s3.45-back and core' 'chin/dip assist'
 'incline chest press' 'seated row' 'incline lever row' 'puzzle mat'    
 'barbell lifter']


