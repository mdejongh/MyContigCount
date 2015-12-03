
package us.kbase.mycontigcount;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: RunFBAResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "flux_value"
})
public class RunFBAResult {

    @JsonProperty("flux_value")
    private Double fluxValue;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("flux_value")
    public Double getFluxValue() {
        return fluxValue;
    }

    @JsonProperty("flux_value")
    public void setFluxValue(Double fluxValue) {
        this.fluxValue = fluxValue;
    }

    public RunFBAResult withFluxValue(Double fluxValue) {
        this.fluxValue = fluxValue;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("RunFBAResult"+" [fluxValue=")+ fluxValue)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
