// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package de.labor23.powercounter.web;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.web.PowerMeterBean;
import java.util.List;

privileged aspect PowerMeterBean_Roo_JavaBean {
    
    public PowerMeter PowerMeterBean.getPowerMeter() {
        return this.powerMeter;
    }
    
    public void PowerMeterBean.setPowerMeter(PowerMeter powerMeter) {
        this.powerMeter = powerMeter;
    }
    
    public List<PowerMeter> PowerMeterBean.getAllPowerMeters() {
        return this.allPowerMeters;
    }
    
    public void PowerMeterBean.setAllPowerMeters(List<PowerMeter> allPowerMeters) {
        this.allPowerMeters = allPowerMeters;
    }
    
    public List<PowerMeter> PowerMeterBean.getUnusedPowerMeters() {
        return this.unusedPowerMeters;
    }
    
    public void PowerMeterBean.setUnusedPowerMeters(List<PowerMeter> unusedPowerMeters) {
        this.unusedPowerMeters = unusedPowerMeters;
    }
    
}