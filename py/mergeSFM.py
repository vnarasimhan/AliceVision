import os, argparse, json

def getValue(di, a, d):
  if (a in di):
    return di[a]
  return d

def map1(oTgtSfm, key, read):
  avail = getValue(oTgtSfm, key, dict())
  for key2 in read:
    if (key2 in avail):
      continue
    avail[key2] = read[key2]
  oTgtSfm[key] = avail
  return oTgtSfm

def extract(oTgtSfm, srcSfm):
  print("Processing %s" % (srcSfm))
  with open(srcSfm, 'r') as fSrcSfm:
    oSrcSfm = json.load(fSrcSfm)
  if (oTgtSfm is None):
    oTgtSfm = dict()

  myViews = dict()
  for view in oSrcSfm["views"]:
    metadata = view["metadata"]
    bodySerial = metadata["Exif:BodySerialNumber"]
    lensSerial = metadata["Exif:LensSerialNumber"]
    key = bodySerial + lensSerial
    myViews[key] = view

  myIntrinsics = dict()
  for intrinsic in oSrcSfm["intrinsics"]:
    key = intrinsic["serialNumber"]
    myIntrinsics[key] = intrinsic

  myPoses = dict()
  for pose in oSrcSfm["poses"]:
    key = pose["poseId"]
    myPoses[key] = pose

  oTgtSfm = map1(oTgtSfm, "views", myViews)
  oTgtSfm = map1(oTgtSfm, "intrinsics", myIntrinsics)
  oTgtSfm = map1(oTgtSfm, "poses", myPoses)

  return oTgtSfm

def save(tgtSfm, oTgtSfm):
  if (tgtSfm is None):
    tgtSfm = "/dev/tty"
    
  result = dict()
  result["version"] = ["1", "0", "0"]
  result["featuresFolders"] = ["features"]
  result["matchesFolders"] = ["matches"]
  result["views"] = list(oTgtSfm["views"].values())
  result["intrinsics"] = list(oTgtSfm["intrinsics"].values())
  result["poses"] = list(oTgtSfm["poses"].values())

  with open(tgtSfm, "w") as fTgtSfm:
    json.dump(result, fTgtSfm, indent=2)

parser = argparse.ArgumentParser(description="Merge intrinsics, poses and views in AliceVision SFM")

parser.add_argument('--srcSfms', type=str, nargs='+', help="One or more source SFMs")
parser.add_argument('--srcSfmList', type=str, help="Text file containing paths to SFM files")
parser.add_argument("--tgtSfm", type=str, help="Target SFM file")
args = parser.parse_args()

oTgtSfm = None
try:
  with open(tgtSfm, 'r') as fTgtSfm:
    oTgtSfm = json.load(fTgtSfm)
except:
  oTgtSfm = None
  
if (args.srcSfmList is not None):
  try:
    with open(args.srcSfmList, 'r') as fSfmList:
      for line in fSfmList:
        oTgtSfm = extract(oTgtSfm, line.strip())
  except:
      pass
elif (args.srcSfms is not None):
  for srcSfm in args.srcSfms:
    oTgtSfm = extract(oTgtSfm, srcSfm)

save(args.tgtSfm, oTgtSfm)
