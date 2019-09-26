#!/bin/sh

fullPath=$(realpath "$0")
scriptDir=$(dirname "$fullPath")

. ${scriptDir}/include.sh
stitchCaptureId=${CAPTURE_ID}
sfmCaptureId=${CAPTURE_ID}
startFrame=1
endFrame=1
nasDataDir=/ext/input/nas-mount/data
framesDir=/ext/input/frames

outputBaseDir=/ext/output/aliceStitches/${stitchCaptureId}

sfmBaseDir=/ext/output/alice/${sfmCaptureId}/frame1
sensorsDb=${AV_BUNDLE}/share/aliceVision/cameraSensors.db 
currentFrame=${startFrame}
cpuOnly=0
numPoses=${NUM_CAMS}
describerTypes=sift,akaze
describerTypes=sift

frameInputDir=${framesDir}/${stitchCaptureId}/genUsable/usable
echo addCameraMeta2 "${frameInputDir}" 1 0
frameDirPrefix=frame
while test ${currentFrame} -le ${endFrame}; do
  echo ${currentFrame}
  frameOutputDir=${outputBaseDir}/${frameDirPrefix}${currentFrame}
  prepareDenseOutputDir=${frameOutputDir}/prepareDense
  mkdir -p ${prepareDenseOutputDir}
  sfmPath=${sfmBaseDir}/incremental.sfm
  echo aliceVision_prepareDenseScene \
    --imagesFolders ${frameInputDir}/${frameDirPrefix}${currentFrame} \
    --input=${sfmPath} \
    --output=${prepareDenseOutputDir}
  estimateDepthOutputDir=${frameOutputDir}/estDepth
  mkdir -p ${estimateDepthOutputDir}
  echo aliceVision_depthMapEstimation \
    --input=${sfmPath} \
    --imagesFolder ${prepareDenseOutputDir} \
    --output=${estimateDepthOutputDir}
  filterDepthOutputDir=${frameOutputDir}/filterDepth
  mkdir -p ${filterDepthOutputDir}
  echo aliceVision_depthMapFiltering \
    --input=${sfmPath} \
    --depthMapsFolder ${estimateDepthOutputDir} \
    --output=${filterDepthOutputDir}
  currentFrame=$(expr ${currentFrame} + 1)
done
