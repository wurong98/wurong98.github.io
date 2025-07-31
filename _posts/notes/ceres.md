# ceres学习笔记

[官方文档](http://ceres-solver.org/nnls_tutorial.html#hello-world)

源码安装ceres

``` bash
git clone https://ceres-solver.googlesource.com/ceres-solver
# 需要更新 git submoudle init/update  third-part有连个依赖lib
make
sudo make install
```

开始helloworld

CMakeLists.txt
```
cmake_minimum_required(VERSION 3.1)

project(helloworld)
find_package(GTest CONFIG REQUIRED)
find_package(absl CONFIG REQUIRED)
find_package(Ceres REQUIRED)
include_directories(${CERES_INCLUDE_DIRS}  ${ABSL_INCLUDE_DIRS} ${GTEST_INCLUDE_DIRS})

# helloworld
add_executable(helloworld helloworld.cc)
target_link_libraries(helloworld absl::log_initialize ${CERES_LIBRARIES} ${ABSL_LIBRARIES} ${GTEST_LIBRARIES})
```

学习过程中测试的代码在[这个代码仓库](https://gitee.com/wu_rong/learning-ceres)