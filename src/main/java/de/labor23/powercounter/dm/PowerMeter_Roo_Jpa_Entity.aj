// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package de.labor23.powercounter.dm;

import de.labor23.powercounter.dm.PowerMeter;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Version;

privileged aspect PowerMeter_Roo_Jpa_Entity {
    
    declare @type: PowerMeter: @Entity(name = "PowerMeter");
    
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id")
    private Long PowerMeter.id;
    
    @Version
    @Column(name = "version")
    private Integer PowerMeter.version;
    
    public Long PowerMeter.getId() {
        return this.id;
    }
    
    public void PowerMeter.setId(Long id) {
        this.id = id;
    }
    
    public Integer PowerMeter.getVersion() {
        return this.version;
    }
    
    public void PowerMeter.setVersion(Integer version) {
        this.version = version;
    }
    
}
