<script lang="ts">
import {scaleLinear, scaleSequential, scaleDiverging} from 'd3-scale';
import {contourDensity} from 'd3-contour';
import {create, select, selectAll} from 'd3-selection';
import {geoPath} from 'd3-geo';
import {interpolateRdBu, schemeRdBu} from 'd3-scale-chromatic';
import {extent} from 'd3-array';
import { pitch_types } from '../assets/pitch_types';


export let width;
export let height;
export let data;

let pitch_data = null;
let data_key_order = ["MPH","Spin","SO","Hits","EV","Whiff %","Chase %"]

var margin = {top: 10, right: 30, bottom: 40, left: 50},
    chartWidth = width/3- margin.left - margin.right,
    chartHeight = height/3 - margin.top - margin.bottom;

var scaleY = scaleLinear([5,-1.5],[margin.bottom,chartHeight-margin.top]);
var scaleX = scaleLinear([-2.5,2.5],[margin.left,chartWidth-margin.right])


function getLength(length,scale){
    return Math.abs(scale(length)-scale(0));
}

function initContour(node, data){
    createContours(data,node.id);
    return{
        update(data){
            select("#"+node.id).select(".contour_svg").remove();
            createContours(data,node.id);
        }
    }
}

function createContours(data,cont_id){
    var contourData = contourDensity()
        .x(function(d:any) { return scaleX(d.plate_x); }) 
        .y(function(d:any) { return scaleY(d.plate_z); })
        .thresholds(10)
        .size([chartWidth,chartHeight])
        .cellSize(1)
        (data)

    var color = scaleDiverging(['#879fcc','#f7f7f7','#eb2f2f']).domain([0,contourData[1].value,contourData[contourData.length-1].value]);

    var contourContainer = select("#"+cont_id);

    var group = contourContainer
    .append("g")
    .attr("class","contour_svg")
    
    group
    .selectAll()
    .data(contourData)
    .join("path")
        .attr("d", geoPath())
        .attr("fill",function(d){ return color(d.value)})
        .attr("stroke", "steelblue")
        .attr("stroke-width",0)
        .attr("stroke-linejoin", "round");

    group.append("rect")
    .attr("width",getLength(1.7,scaleX))
    .attr("height", getLength(1.9,scaleY))
    .attr("x", scaleX(-0.85))
    .attr("y", scaleY(3.6))
    .attr("fill", 'none')
    .attr("style", "stroke-width:1;stroke:black" )
}

async function pitchDataSearch(query){
    fetch('./api/player_pitch_data/'+query)
      .then(d => d.json())
      .then(d => (pitch_data = d))
  }

function sortPitchesByPitchCount(a,b){
    let sum_a = data.reduce((acc,curr)=>acc + (curr.pitch_type === a.abbv ? 1 : 0),0);
    let sum_b = data.reduce((acc,curr)=>acc + (curr.pitch_type === b.abbv ? 1 : 0), 0);
    return sum_b-sum_a
}

    $: pitchDataSearch(data[0].pitcher_id);
</script>

<div class="contour_collection">
    {#each pitch_types.sort(sortPitchesByPitchCount) as type, index}
        {@const filtered_data = data.filter((d=>d.pitch_type === type.abbv))}
        {#if filtered_data.length > 0}
        <div class="contour_data_container">
            <div class="contour_header">
                <b>{type.name}</b><br>
                {filtered_data.length} pitches ({Math.round(filtered_data.length/data.length*1000)/10}%{index===0?' of all pitches':''})
            </div>
            <div class="chart_table_container">
                <svg use:initContour={filtered_data} width={chartWidth} height={chartHeight} id={"contours_"+type.abbv}>
                </svg>
                {#if pitch_data}
                    {@const pitch_averages = pitch_data.find((d)=>d.pitch_type===type.abbv)}
                    <div class="pitch_table">
                        <table>
                            <tbody>
                                {#each data_key_order as category}
                                    {#if category != 'pitch_type'}
                                    <tr>
                                        <td>{category}</td>
                                        <td>{pitch_averages[category]}</td>
                                    </tr>
                                    {/if}
                                {/each}
                            </tbody>
                        </table>
                    </div>
                {/if}
            </div>
        </div>
        {/if}
    {/each}
</div>

<style>
    .contour_collection{
        display: flex;
        justify-content: space-around;
        color:black;
        flex-wrap: wrap;
        max-width: 100vw;
    }
    .contour_collection > *{
        min-width: 400px;
    }
    .chart_table_container{
        display:grid;
        grid-template-columns:50% 50%;
    }
    .pitch_table{
        margin-top:10px;
    }
    .contour_data_container{
        margin-bottom: 10px;
    }
</style>


