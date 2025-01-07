<script lang="ts">
import {scaleLinear, scaleSequential, scaleDiverging} from 'd3-scale';
import {contourDensity} from 'd3-contour';
import {create, select} from 'd3-selection';
import {geoPath} from 'd3-geo';
import {interpolateRdBu, schemeRdBu} from 'd3-scale-chromatic';
import {extent} from 'd3-array';

export let data;

var margin = {top: 10, right: 30, bottom: 40, left: 50},
    width = 520 - margin.left - margin.right,
    height = 520 - margin.top - margin.bottom;

var scaleY = scaleLinear([5,0],[margin.bottom,height-margin.top]);
var scaleX = scaleLinear([-2.5,2.5],[margin.left,width-margin.right])

function getLength(length,scale){
    return Math.abs(scale(length)-scale(0));
}

function initContour(node, data){
    createContours(data);
    return{
        update(data){
            select("#contours").selectAll("*").remove();
            createContours(data);
        }
    }
}

function createContours(data){
    var contourData = contourDensity()
        .x(function(d:any) { return scaleX(d.plate_x); }) 
        .y(function(d:any) { return scaleY(d.plate_z); })
        .thresholds(10)
        .size([width,height])
        .cellSize(1)
        (data)

    // var color = scaleSequential
    //     .domain(extent(contourData.map((d)=>d.value)).reverse())
    //     .range(['#b2182b','#2166ac']) // Points per square pixel.
    console.log(contourData);

    var color = scaleDiverging(['#879fcc','#f7f7f7','#eb2f2f']).domain([0,contourData[3].value,contourData[contourData.length-1].value]);

    var contourContainer = select("#contours");

    contourContainer
    .selectAll()
    .data(contourData)
    .join("path")
        .attr("d", geoPath())
        .attr("fill",function(d){ return color(d.value)})
        .attr("stroke", "steelblue")
        .attr("stroke-width",0)
        .attr("stroke-linejoin", "round");
}

</script>

<div>
    <svg width=520 height=520>
        <!-- contours -->
        <g use:initContour={data} id="contours"></g> 
        <!-- strikezone -->
        <rect 
            width={getLength(1.7,scaleX)}
            height={getLength(1.9,scaleY)}
            x={scaleX(-0.85)}
            y={scaleY(3.6)}
            fill=none
            style="stroke-width:1;stroke:black" 
        >
        </rect>
    </svg>
</div>


