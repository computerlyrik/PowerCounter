// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package de.labor23.powercounter.web;

import de.labor23.powercounter.web.LiveBean;
import java.util.List;

privileged aspect LiveBean_Roo_JavaBean {
    
    public List<Number> LiveBean.getIntervals() {
        return this.intervals;
    }
    
    public void LiveBean.setIntervals(List<Number> intervals) {
        this.intervals = intervals;
    }
    
}