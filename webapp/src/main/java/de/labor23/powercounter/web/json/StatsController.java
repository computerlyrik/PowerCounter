package de.labor23.powercounter.web.json;
import java.util.Calendar;

import org.apache.log4j.Logger;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.roo.addon.web.mvc.controller.json.RooWebJson;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import de.labor23.powercounter.dm.Tick;
import de.labor23.powercounter.dm.json.TickDTO;
import de.labor23.powercounter.web.util.WattageCalculatorUtil;

@RooWebJson(jsonObject = TickDTO.class)
@Controller
@RequestMapping("/stats")
public class StatsController {
	
	private final Logger log = Logger.getLogger(StatsController.class);
	
	
    @RequestMapping(value = "/overall", method = RequestMethod.GET, headers = "Accept=application/json")
    @ResponseBody
    public ResponseEntity<String> showOverallPerformance() {
    	
    	Long watt = WattageCalculatorUtil.getCurrentWatts(10);

        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json; charset=utf-8");

        return new ResponseEntity<String>("{\"overall\":"+watt+"}", headers, HttpStatus.OK);
    }
}
