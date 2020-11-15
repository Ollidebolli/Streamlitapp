import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import math
from functools import reduce

st.title('Elenas thing')

Q1 = st.selectbox(
    'Does your organization have a vision statement, mission statement, and a list of values?',
    ["No","Yes"]
    )

if Q1 == "Yes":

    Q2 = st.radio(
        'Does your organization expand its products and operations incrementally (e.g. pause,proceed, pause, proceed), or continuously (e.g. go, go, go)?',
        ("INCREMENTALLY","CONTINUOUSLY")
        )
    Q3 = st.radio(
        'How clear and supportive are the employees of the vision, mission, and values of the organization?',
        ('UNCLEAR & UNSUPPORTIVE',
        'UNCLEAR, but SUPPORTIVE',
        'CLEAR & SUPPORTIVE',
        'CLEAR, but UNSUPPORTIVE')
        )
    Q4 = st.radio(
        'How likely is the management to align every decision with the vision, mission, and values of the organization?',
        ('VERY UNLIKELY',
        'UNLIKELY',
        'LIKELY',
        'VERY LIKELY')
        )

    if Q3 == 'UNCLEAR & UNSUPPORTIVE': s_point_y = 7.5
    elif Q3 == 'UNCLEAR, but SUPPORTIVE': s_point_y = 2.5
    elif Q3 == 'CLEAR & SUPPORTIVE': s_point_y = -2.5
    elif Q3 == 'CLEAR, but UNSUPPORTIVE': s_point_y = -7.5

    if Q4 == 'VERY UNLIKELY': s_point_x = -7.5
    elif Q4 == 'UNLIKELY': s_point_x = -2.5
    elif Q4 == 'LIKELY': s_point_x = 2.5
    elif Q4 == 'VERY LIKELY': s_point_x = 7.5

#Axis oriented
Q5 = st.slider(
    'On a scale from 1 to 10, how much does your organization value any initiatives, that benefit the wellbeing of the society? (TrF +)',1,10,5)
Q6 = st.slider(
    'On a scale from 1 to 10, How much does your organization utilize industry reports and historical analysis for decision making? (TrA-)',1,10,5)
Q7 = st.slider(
    'On a scale from 1 to 10, how well does your organization learn from mistakes? (TrF-)',1,10,5)
Q8 = st.slider(
    'On a scale from 1 to 10, how likely is your organization to adopt innovative technological and financial solutions, that have not been fully endorsed by the majority market yet? (TrA+)',1,10,5)
Q9 = st.slider(
    'On a scale from 1 to 10, how aggressive is your organization with the long-term sales plan? (Strategy, TrA)',1,10,5)
Q10 = st.slider(
    'On a scale from 1 to 10, how disruptive does your organization aspire to be in its industry? (Strategy, TrF)',1,10,5)
Q11 = st.slider(
    'On a scale from 1 to 10, how consistent is your organization with HR policies in a verbal, written, and non-verbal form? (Culture, TrA)',1,10,5)
Q12 = st.slider(
    'On a scale from 1 to 10, how likely is your organization to promote and support employee personal growth? (Culture, TrF)',1,10,5)
Q13 = st.slider(
    'On a scale from 1 to 10, how reliable and accurate is the data collected through your organization’s operational and accounting systems? (Data, TrA)',1,10,5)
Q14 = st.slider(
    'On a scale from 1 to 10, how well does your organization analyze various internal and external information to make decisions? (Data, TrF)',1,10,5)
Q15 = st.slider(
    'On a scale from 1 to 10, how easy is it to follow the chain of processes in your organization? (Structure, TrA)',1,10,5)
Q16 = st.slider(
    'On a scale from 1 to 10, how easy is it to make the suggestions to the superiors on procedural changes in your organization? (Structure, TrF)', 1,10,5)

@st.cache(suppress_st_warning=True)
def visualize(s_point_x,s_point_y,Q2,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16):

    if Q1 == "Yes":
        X = [s_point_x,0,-Q6,0,Q8,Q9,-Q11,-Q13,Q15]
        Y = [s_point_y,Q5,0,-Q7,0,Q10,Q12,-Q14,-Q16]
        
    else:
        X = [0,-Q6,0,Q8,Q9,-Q11,-Q13,Q15]
        Y = [Q5,0,-Q7,0,Q10,Q12,-Q14,-Q16]


    def squared_polar(point, center):
        angle = math.atan2(point['y'] - center['y'], point['x'] - center['x'])
        distance = (point['x'] - center['x'])**2 + (point['y'] - center['y'])**2
        return angle, distance

    def sort_point(point):
        angle, distance = squared_polar(point, points_center)
        return angle if angle != 0 else distance

    a = pd.DataFrame({
        'x':X,
        'y':Y})

    points = a.to_dict('records')

    points_center = {
    'x': reduce((lambda x,p: p['x'] + x), points, 0) / len(points),
    'y': reduce((lambda y,p: p['x'] + y), points, 0) / len(points),
    }

    sorted_points = sorted(points, key=lambda x: sort_point(x))

    b = pd.DataFrame(sorted_points)

    fig, ax = plt.subplots(figsize=(10,10))

    ax.set_yticks([0], minor=False)
    ax.yaxis.grid(True, which='major')
    ax.set_xticks([0], minor=False)
    ax.xaxis.grid(True, which='major')

    #Plot the polygon
    if Q1 == "Yes":
        if (Q3 =='UNCLEAR & UNSUPPORTIVE') & (Q4 == 'VERY UNLIKELY'):
            polygon = Polygon(np.array(b), fill=False)
        elif (Q3 =='CLEAR & SUPPORTIVE') & (Q4 == 'VERY LIKELY'):
            polygon = Polygon(np.array(b), alpha = 0.4, fill=True)
        else:
            polygon = Polygon(np.array(b),fill=False, hatch='/')
    else:
        polygon = Polygon(np.array(b), alpha = 0.4, fill=True)

    ax.add_patch(polygon)
    ax.set_xlim([-10,10])
    ax.set_ylim([-10,10])

    #plot the spiral
    if  (Q1 == 'Yes') & (Q2 == "CONTINUOUSLY"):

        n = 800
        radius = max(np.abs([Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16]))

        angle = np.linspace(0,5*2*np.pi, n)
        radius = np.linspace(0,radius,n)

        x = radius * np.cos(angle)
        y = radius * np.sin(angle)

        ax2 = ax.twinx()
        ax2.scatter(x,y, c = angle)
        ax2.set_xlim([-10,10])
        ax2.set_ylim([-10,10])
    

    #Plot the circles
    elif  (Q1 == 'Yes') & (Q2 == "INCREMENTALLY"):

        ax3 = ax.twinx()

        radius1 = max(np.abs([Q5,Q6,Q7,Q8]))
        radius2 = max(np.abs([Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16]))
        ax3.add_artist(plt.Circle((0, 0), radius1, fill=False, lw=2))
        ax3.add_artist(plt.Circle((0, 0), radius2, fill=False, lw=2))
        ax3.set_xlim([-10,10])
        ax3.set_ylim([-10,10])


    plt.xlabel('TrA (Transaction)', fontsize=10)
    plt.ylabel('TrF (Transformation)', fontsize=10)
    img = plt.imread("BG.png")
    ax.imshow(img,extent=[-10,10,-10,10])

    

    st.write(fig)



if st.button('Visualize'): 

    if Q1 == "Yes":
        visualize(s_point_x,s_point_y,Q2,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16)
    elif Q1 == "No":
        Q2=1
        visualize(10,10,Q2,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16)