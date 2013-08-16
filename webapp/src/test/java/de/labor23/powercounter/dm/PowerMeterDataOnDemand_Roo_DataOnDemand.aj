// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package de.labor23.powercounter.dm;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.dm.PowerMeterDataOnDemand;
import de.labor23.powercounter.dm.User;
import de.labor23.powercounter.dm.hardware.Bank;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import javax.validation.ConstraintViolation;
import javax.validation.ConstraintViolationException;
import org.springframework.stereotype.Component;

privileged aspect PowerMeterDataOnDemand_Roo_DataOnDemand {
    
    declare @type: PowerMeterDataOnDemand: @Component;
    
    private Random PowerMeterDataOnDemand.rnd = new SecureRandom();
    
    private List<PowerMeter> PowerMeterDataOnDemand.data;
    
    public PowerMeter PowerMeterDataOnDemand.getNewTransientPowerMeter(int index) {
        PowerMeter obj = new PowerMeter();
        setAddress(obj, index);
        setBank(obj, index);
        setMeterName(obj, index);
        setTicksPerKWH(obj, index);
        setUser(obj, index);
        return obj;
    }
    
    public void PowerMeterDataOnDemand.setAddress(PowerMeter obj, int index) {
        Byte address = new Byte("1");
        obj.setAddress(address);
    }
    
    public void PowerMeterDataOnDemand.setBank(PowerMeter obj, int index) {
        Bank bank = Bank.class.getEnumConstants()[0];
        obj.setBank(bank);
    }
    
    public void PowerMeterDataOnDemand.setMeterName(PowerMeter obj, int index) {
        String meterName = "meterName_" + index;
        obj.setMeterName(meterName);
    }
    
    public void PowerMeterDataOnDemand.setTicksPerKWH(PowerMeter obj, int index) {
        Integer ticksPerKWH = new Integer(index);
        obj.setTicksPerKWH(ticksPerKWH);
    }
    
    public void PowerMeterDataOnDemand.setUser(PowerMeter obj, int index) {
        User user = null;
        obj.setUser(user);
    }
    
    public PowerMeter PowerMeterDataOnDemand.getSpecificPowerMeter(int index) {
        init();
        if (index < 0) {
            index = 0;
        }
        if (index > (data.size() - 1)) {
            index = data.size() - 1;
        }
        PowerMeter obj = data.get(index);
        Long id = obj.getId();
        return PowerMeter.findPowerMeter(id);
    }
    
    public PowerMeter PowerMeterDataOnDemand.getRandomPowerMeter() {
        init();
        PowerMeter obj = data.get(rnd.nextInt(data.size()));
        Long id = obj.getId();
        return PowerMeter.findPowerMeter(id);
    }
    
    public boolean PowerMeterDataOnDemand.modifyPowerMeter(PowerMeter obj) {
        return false;
    }
    
    public void PowerMeterDataOnDemand.init() {
        int from = 0;
        int to = 10;
        data = PowerMeter.findPowerMeterEntries(from, to);
        if (data == null) {
            throw new IllegalStateException("Find entries implementation for 'PowerMeter' illegally returned null");
        }
        if (!data.isEmpty()) {
            return;
        }
        
        data = new ArrayList<PowerMeter>();
        for (int i = 0; i < 10; i++) {
            PowerMeter obj = getNewTransientPowerMeter(i);
            try {
                obj.persist();
            } catch (final ConstraintViolationException e) {
                final StringBuilder msg = new StringBuilder();
                for (Iterator<ConstraintViolation<?>> iter = e.getConstraintViolations().iterator(); iter.hasNext();) {
                    final ConstraintViolation<?> cv = iter.next();
                    msg.append("[").append(cv.getRootBean().getClass().getName()).append(".").append(cv.getPropertyPath()).append(": ").append(cv.getMessage()).append(" (invalid value = ").append(cv.getInvalidValue()).append(")").append("]");
                }
                throw new IllegalStateException(msg.toString(), e);
            }
            obj.flush();
            data.add(obj);
        }
    }
    
}
