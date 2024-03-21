import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
random.seed(a=1)

constant_1 = 1.39 #np.sqrt(2*900/938) 
constant_2= 0.5211 #938/1800 

def detector_generator(angle, distance, lenght): #angles in degrees, distance in cm, lenght and height in cm
    m= np.tan(np.radians(angle))
    intercept = distance*np.sin(np.radians(angle))+distance*np.cos(np.radians(angle))/m
    a = 1+1/(m**2)
    b = 2*(-distance*np.cos(np.radians(angle))+distance*np.sin(np.radians(angle))/m-intercept/m)
    c = intercept**2-lenght**2/4-2*distance*intercept*np.sin(np.radians(angle))+distance**2
    x_1, x_2 = (-b+np.sqrt(np.abs(b**2-4*a*c)))/(2*a), (-b-np.sqrt(np.abs(b**2-4*a*c)))/(2*a)
    y_1, y_2 = -x_1/m+intercept, -x_2/m+intercept
    angle_1, angle_2 = np.degrees(np.arctan2(y_1,x_1)), np.degrees(np.arctan2(y_2,x_2))
    x_graph = np.linspace(x_1, x_2, 1000)
    y_graph = [-i/m+intercept for i in x_graph]
    d_graph_x = np.linspace(0, distance, 1000)
    d_graph_y = [i*m for i in d_graph_x]
    return angle_1, angle_2, np.radians(angle), distance, x_graph, y_graph, d_graph_x, d_graph_y

def TOF_measure(angle_measure, detector_start, detector_stop, v):
    x_start, x_stop = detector_start[3]*np.tan(np.radians(np.abs(detector_start[2]-angle_measure))), detector_stop[3]*np.tan(np.radians(np.abs(detector_stop[2]-angle_measure)))
    flight_path = np.sqrt((detector_stop[3]-detector_start[3])**2+(x_start-x_stop)**2)
    TOF = flight_path/v
    return TOF, x_start, x_stop, flight_path

def TOF(measurements_t, measurements_p, velocities_t, velocities_p, detector_start_t, detector_stop_t, detector_start_p, detector_stop_p): #assuming detectors are aligned
    detection, detection_single_t, detection_single_p = [], [], []
    stsp_t, stsp_p = [], []
    min_t_start, max_t_start = np.min([detector_start_t[0],detector_start_t[1]]), np.max([detector_start_t[0],detector_start_t[1]])
    min_t_stop, max_t_stop = np.min([detector_stop_t[0],detector_stop_t[1]]), np.max([detector_stop_t[0],detector_stop_t[1]])
    min_p_start, max_p_start = np.min([detector_start_p[0],detector_start_p[1]]), np.max([detector_start_p[0],detector_start_p[1]])
    min_p_stop, max_p_stop = np.min([detector_stop_p[0],detector_stop_p[1]]), np.max([detector_stop_p[0],detector_stop_p[1]])
    for i in range(len(measurements_t)):
        TOF_t_total = TOF_measure(measurements_t[i], detector_start_t, detector_stop_t, velocities_t[i])
        TOF_p_total = TOF_measure(measurements_p[i], detector_start_p, detector_stop_p, velocities_p[i])
        TOF_t, x_start_t, x_stop_t = TOF_t_total[0], TOF_t_total[1], TOF_t_total[2]
        TOF_p, x_start_p, x_stop_p = TOF_p_total[0], TOF_p_total[1], TOF_p_total[2]
        #cross-detection
        if np.abs(detector_start_t[0])>np.abs(detector_stop_p[0]) and np.abs(detector_start_p[0])>np.abs(detector_stop_p[0]):
            if min_t_start<=measurements_t[i]<=max_t_start and min_p_start<=measurements_p[i]<=max_p_start:
                detection.append([measurements_t[i], measurements_p[i], TOF_t, TOF_p])
        elif np.abs(detector_start_t[0])>np.abs(detector_stop_p[0]) and np.abs(detector_start_p[0])<=np.abs(detector_stop_p[0]):
            if min_t_start<=measurements_t[i]<=max_t_start and min_p_stop<=measurements_p[i]<=max_p_stop:
                detection.append([measurements_t[i], measurements_p[i], TOF_t, TOF_p])
        elif np.abs(detector_start_t[0])<=np.abs(detector_stop_p[0]) and np.abs(detector_start_p[0])>np.abs(detector_stop_p[0]):
            if min_t_stop<=measurements_t[i]<=max_t_stop and min_p_start<=measurements_p[i]<=max_p_start:
                detection.append([measurements_t[i], measurements_p[i], TOF_t, TOF_p])
        else:
            if min_t_stop<=measurements_t[i]<=max_t_stop and min_p_stop<=measurements_p[i]<=max_p_stop:
                detection.append([measurements_t[i], measurements_p[i], TOF_t, TOF_p])

        #single-detections
        if np.abs(min_t_start)>np.abs(min_t_stop) and min_t_start<=measurements_t[i]<=max_t_start:
            detection_single_t.append([measurements_t[i],TOF_t])
            stsp_t.append([measurements_t[i], (x_start_t - x_stop_t)**2])
        elif np.abs(min_t_start)<=np.abs(min_t_stop) and min_t_stop<=measurements_t[i]<=max_t_stop:
            detection_single_t.append([measurements_t[i],TOF_t])
            stsp_t.append([measurements_t[i], (x_start_t - x_stop_t)**2])
        if np.abs(min_p_start)>np.abs(min_p_stop) and min_p_start<=measurements_p[i]<=max_p_start:
            detection_single_p.append([measurements_p[i], TOF_p])
            stsp_p.append([measurements_p[i], (x_start_p - x_stop_p)**2])
        elif np.abs(min_p_start)<=np.abs(min_p_stop) and min_p_stop<=measurements_p[i]<=max_p_stop:
            detection_single_p.append([measurements_p[i], TOF_p])
            stsp_p.append([measurements_p[i], (x_start_p - x_stop_p)**2])
    
    return detection, detection_single_t, detection_single_p, stsp_t, stsp_p


def v_cm_function(m_1, m_2, E):
    value = constant_1*np.sqrt((E*m_1)/((m_1+m_2)*m_2))
    return value

def v_lab_function(theta_cm, v, v_cm):
    value = np.sqrt((v*np.sin(np.radians(theta_cm)))**2+(v*np.cos(np.radians(theta_cm))+v_cm)**2)
    return value

def theta_targ_lab_function(theta_cm_deg):
    theta_cm_rad = theta_cm_deg*np.pi/180
    if np.cos(theta_cm_rad)==-1:
        return 180
    else:
        return np.degrees(np.arctan(np.sin(theta_cm_rad)/(1+np.cos(theta_cm_rad))))
    
def theta_proj_lab_function(theta_cm_deg, m_p, m_T):
    theta_cm_rad = theta_cm_deg*np.pi/180
    conversion = np.sin(theta_cm_rad)/(m_p/m_T+np.cos(theta_cm_rad))
    if conversion<=0:
        return np.degrees(np.arctan(conversion))
    else:
        return -180+np.degrees(np.arctan(conversion))


def ruth_diff(theta, z_p, z_T, E_lab, alpha=1/137, hc=197):
    return (z_p*z_T*alpha*hc/(4*E_lab*(np.sin(np.radians(theta/2)))**2))**2*10 #millibarn


def MC(N, theta_p_lab, E_lab_0, inc_E_lab, z_p, z_T, theta_min, theta_max):
    angles = []
    for i in theta_p_lab:
        if theta_min<=i<=theta_max:
            angles.append(i)
    energies = [E_lab_0+random.gauss(0, inc_E_lab) for i in range(len(angles))]
    cross_section = [ruth_diff(angles[i], z_p, z_T, energies[i]) for i in range(len(angles))]
    normalization = np.sum(cross_section)
    data = []
    for i in range(0, len(cross_section)-1):
        t_min, t_max = np.sum(cross_section[:i])/normalization, np.sum(cross_section[:i+1])/normalization
        data.append([angles[i], energies[i], cross_section[i], t_min, t_max])
    output_angles, output_energies = [], []
    for i in range(N):
        t = random.uniform(0, 1)
        for j in range(len(data)):
            if data[j][3]<=t<=data[j][4]:
                output_angles.append(data[j][0])
                output_energies.append(data[j][1])
    return output_angles, output_energies


def execute(m_p, m_T, z_p, z_T, E_lab_0, inc_E_lab,
            angle_start_arm_1, distance_start_arm_1, lenght_start_arm_1,
            angle_stop_arm_1, distance_stop_arm_1, lenght_stop_arm_1,
            angle_start_arm_2, distance_start_arm_2, lenght_start_arm_2,
            angle_stop_arm_2, distance_stop_arm_2, lenght_stop_arm_2):
    start_1 = detector_generator(angle_start_arm_1, distance_start_arm_1, lenght_start_arm_1)
    stop_1 = detector_generator(angle_stop_arm_1, distance_stop_arm_1, lenght_stop_arm_1)
    start_2 = detector_generator(angle_start_arm_2, distance_start_arm_2, lenght_start_arm_2)
    stop_2 = detector_generator(angle_stop_arm_2, distance_stop_arm_2, lenght_stop_arm_2)

    #Applying MC on preview angles
    theta_t_cm_preview = np.arange(0,180,0.01)
    theta_p_lab_preview = [theta_proj_lab_function(-180+i, 40, 208) for i in theta_t_cm_preview]
    min_angular, max_angular = np.max([np.abs(start_2[0]), np.abs(stop_2[0])]), np.min([np.abs(start_2[1]), np.abs(stop_2[1])])
    if np.max(theta_p_lab_preview)<=0:
        theta_p_lab_mc, E_lab_mc = MC(10000, theta_p_lab_preview, E_lab_0, inc_E_lab, z_p, z_T, -max_angular, -min_angular) #in the case of negative angles min and max swap
    else:
        theta_p_lab_mc, E_lab_mc = MC(10000, theta_p_lab_preview, E_lab_0, inc_E_lab, z_p, z_T, min_angular, max_angular)
    #sorting the angles chosen by the MC
    theta_t_cm = []
    E_lab =[]
    for i in range(len(theta_p_lab_mc)):
        for j in range(len(theta_p_lab_preview)):
            if theta_p_lab_mc[i] == theta_p_lab_preview[j]:
                theta_t_cm.append(theta_t_cm_preview[j])
                E_lab.append(E_lab_mc[i])
    theta_p_lab = [theta_proj_lab_function(-180+i, m_p, m_T) for i in theta_t_cm]
    theta_t_lab = [theta_targ_lab_function(i) for i in theta_t_cm]
    #what was just done is selecting from the theta_t_cm list, only the angles corresponding to theta_p_lab chosen by the MC
    E_cm = [i*m_T/(m_p+m_T) for i in E_lab]
    v_cm = [constant_1*np.sqrt(i*m_p)/(m_p+m_T) for i in E_lab] #cm/ns
    v_p_cm= [v_cm_function(m_T, m_p, i) for i in E_cm]
    v_t_cm= [v_cm_function(m_p, m_T, i) for i in E_cm]
    v_p_lab = [v_lab_function(-180+theta_t_cm[i], v_p_cm[i], v_cm[i]) for i in range(len(theta_t_cm))]
    v_t_lab = [v_lab_function(theta_t_cm[i], v_t_cm[i], v_cm[i]) for i in range(len(theta_t_cm))] 
    #print(np.max(v_p_lab), np.max(v_t_lab))
    E_p_lab = [constant_2*m_p*v_p_lab[i]**2 for i in range(len(v_p_lab))]
    E_t_lab = [constant_2*m_T*v_t_lab[i]**2 for i in range(len(v_t_lab))]
    detection = TOF(theta_t_lab, theta_p_lab, v_t_lab, v_p_lab, start_1, stop_1, start_2, stop_2)
    #print(len(theta_t_cm), len(theta_p_lab), len(theta_t_lab), len(E_lab), len(v_p_lab), len(v_t_lab), len(E_p_lab), len(E_t_lab))
    print('objects created')
    df_mapping = {
        'theta_p_cm': [-180+i for i in theta_t_cm],
        'theta_t_cm': theta_t_cm,
        'theta_p_lab': theta_p_lab,
        'theta_t_lab': theta_t_lab,
        'E_lab': E_lab,
        'v_p_lab': v_p_lab,
        'v_t_lab': v_t_lab,
        'E_p_lab': E_p_lab,
        'E_t_lab': E_t_lab
    }
    dt_mapping = {
        'detection_arm_1_angle': [i[0] for i in detection[0]],
        'detection_arm_2_angle': [i[1] for i in detection[0]],
        'detection_arm_1_tof': [i[2] for i in detection[0]],
        'detection_arm_2_tof': [i[3] for i in detection[0]],
        'detection_arm_1_angle_single': [i[0] for i in detection[1]],
        'detection_arm_2_angle_single': [i[0] for i in detection[2]],
        'detection_arm_1_tof_single': [i[1] for i in detection[1]],
        'detection_arm_2_tof_single': [i[1] for i in detection[2]]
    }
    df = pd.DataFrame(data=df_mapping)
    dt = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in dt_mapping.items()]))
    graph_mapping = {
        'x_graph_1_start': start_1[4],
        'y_graph_1_start': start_1[5],
        'x_graph_2_start': start_2[4],
        'y_graph_2_start': start_2[5],
        'x_graph_1_stop': stop_1[4],
        'y_graph_1_stop': stop_1[5],
        'd_graph_x_1_stop': stop_1[6],
        'd_graph_y_1_stop': stop_1[7],
        'x_graph_2_stop': stop_2[4],
        'y_graph_2_stop': stop_2[5],
        'd_graph_x_2_stop': stop_2[6],
        'd_graph_y_2_stop': stop_2[7]
    }
    graph = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in graph_mapping.items()]))
    print('dataframe created')
    return df, dt, graph


