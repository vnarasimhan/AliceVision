BUILD_TYPE=Debug
NPROC=4
cd ${AV_BUILD}
cmake "${AV_DEV}" -DCMAKE_BUILD_TYPE=${BUILD_TYPE} -DALICEVISION_BUILD_DEPENDENCIES:BOOL=ON -DAV_BUILD_LAPACK:BOOL=OFF -DAV_BUILD_SUITESPARSE:BOOL=OFF -DCMAKE_INSTALL_PREFIX="${AV_INSTALL}" -DALICEVISION_BUNDLE_PREFIX="${AV_BUNDLE}"
cd ${AV_BUILD}
make -j${NPROC} install && make bundle
