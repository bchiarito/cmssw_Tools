get_failed_jobs() {
    crab status --long $1 | grep failed | grep -v code | awk '{print $1}' | grep -v Jobs | tr '\n' , | awk '{print substr($0, 1, length($0)-1)}'
}

resubmit_failed() {
    crab resubmit $1 --jobids=`get_failed_jobs $1`
}
