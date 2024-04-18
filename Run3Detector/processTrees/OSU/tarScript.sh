source ../../setup.sh


gitTag=$(git describe)
arrIN=(${gitTag//-/ })
outputName="milliqanOffline_"${arrIN[0]}'.tar.gz'

SHORT_TAG=$(git describe --tag --abbrev=0)
LONG_TAG=$(git describe --tags --long)

cp $OFFLINEDIR/compile.sh $OFFLINEDIR/compileForBatch.sh
sed -i "s/SHORT_TAG=.*/SHORT_TAG=${SHORT_TAG}/g" $OFFLINEDIR/compileForBatch.sh
sed -i "s/LONG_TAG=.*/LONG_TAG=${LONG_TAG}/g" $OFFLINEDIR/compileForBatch.sh

startingDir=${PWD}
cd $OFFLINEDIR
echo $PWD
cd ../..
tar -zcvf ${outputName} milliqanOffline/Run3Detector/src milliqanOffline/Run3Detector/interface milliqanOffline/Run3Detector/scripts milliqanOffline/Run3Detector/setup.sh milliqanOffline/Run3Detector/compileForBatch.sh milliqanOffline/Run3Detector/configuration
cd $startingDir
mv ~/${outputName} .
