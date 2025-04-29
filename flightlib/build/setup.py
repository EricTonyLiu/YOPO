from setuptools import setup, Extension

#
setup(name='flightgym_adapt',
      version='0.0.1',
      author="Junjie Lu / Yunlong Song / Zihan Liu ",
      author_email='lqzx1998@tju.edu.cn / song@ifi.uzh.ch / 23s053065@stu.hit.edu.cn',
      description="Flightmare: A Quadrotor Simulator ",
      long_description='This project is modified based on Flightmare by Yunlong Song, Thanks for his excellent work! Modified the project for adaptive planning',
      packages=[''],
      package_dir={'': './'},
      package_data={'': ['flightgym_adapt.cpython-38-x86_64-linux-gnu.so']},
      zip_fase=True,
      url=None,
)
