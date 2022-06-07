import streamlit as st
from PIL import Image

# """blog streamlit how to build a sreal time live dashboard with streamlit"""

img = Image.open(R"C:\VisualStudioCode\Data_Orac\getsitelogo.png")

st.title('hello__This is a test-page')
st.image(img, width=200)

# test voor graph
from tkinter import Y
import matplotlib.pyplot as plt
import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import plotly.express as px

X = np.linspace(-5,5,50)
Y = np.linspace(-5,5,50)

X, Y = np.meshgrid(X, Y)


def func(x, y):
    # return np.sin(.5*x/4) + np.cos(1+y/3)  # kwadratic function
    return x**2 + y**2 + x*y + 50*y + 0*x  # standard surface

Z = func(X, Y)

def visual():
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax = fig.gca()

    colorlist = ['PiYG', 'coolwarm', 'winter', 'YlGn']
    # ax.plot_surface(X, Y, Z, cmap=cm.PiYG, alpha=0.5)
    # ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    ax.plot_surface(X, Y, Z, cmap=cm.winter, alpha=0.5)
    CS = ax.contour(X, Y, Z, cmap=cm.winter)
    ax.contour(X, Y, Z, cmap=cm.YlGn)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    # ax.clabel(CS, CS.levels, fontsize=10)
    ax.set_zlabel('result')

    st.pyplot(fig)

visual()