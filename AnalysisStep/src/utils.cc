#include <HTauTauHMuMu/AnalysisStep/interface/utils.h>


namespace htautauhmumu {
  TLorentzVector tlv(const math::XYZTLorentzVector& v){
    return TLorentzVector(v.x(),v.y(),v.z(),v.t());
  }
}
int SetupToSqrts(int setup) {
  if      (setup>=2015&&setup<=2018) return 13;
  else if (setup==2012) return 8;
  else if (setup==2011) return 7;
  else return 0;
}
