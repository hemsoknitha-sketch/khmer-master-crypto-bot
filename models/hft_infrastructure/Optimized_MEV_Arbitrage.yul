
object "MEVArbitrageV2" {
    code {
        datacopy(0, dataoffset("runtime"), datasize("runtime"))
        return(0, datasize("runtime"))
    }
    object "runtime" {
        code {
            calldatacopy(0, 0, calldatasize())
            let success1 := call(gas(), 0x1111111111111111111111111111111111111111, 0, 0, 0x44, 0, 0)
            let success2 := call(gas(), 0x2222222222222222222222222222222222222222, 0, 0, 0x44, 0, 0)
            if iszero(and(success1, success2)) {
                revert(0, 0)
            }
            return(0, 0)
        }
    }
}
