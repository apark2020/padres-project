<script>
import {scaleLinear, scaleSequential, scaleDiverging} from 'd3-scale';
import { pitch_types } from '../assets/common_types';
import { selectAll } from 'd3-selection'

export let data;

var margin = {top: 0, right: 20, bottom: 40, left: 20},
    width = 340,
    height = 400;

var scaleY = scaleLinear([5.5,-1.7],[margin.bottom,height-margin.top]);
var scaleX = scaleLinear([-3,3],[margin.left,width-margin.right]);

let tooltipInfo;

function getLength(length,scale){
    return Math.abs(scale(length)-scale(0));
}

let filters = {
    'pitch_type':'all',
    'batter_side':'all',
    'ball_call':'all',
}

function changePitch(newValue,type){
    filters[type] = newValue;
    selectAll('.scatter_circles circle')
        .each(function(d){
            let turnedZero = false;
            for(const [filter,value] of Object.entries(filters)){
                if (this.getAttribute('data-'+filter) !== value && value !== 'all'){
                    if(!turnedZero && value==="all_strikes" && (this.getAttribute('data-ball_call') === "swinging_strike" || this.getAttribute('data-ball_call') === "called_strike")){
                        this.classList.remove('zero-opacity');
                    }
                    else{
                        this.classList.add('zero-opacity')
                        turnedZero = true;
                    }
                }
            }
            if(!turnedZero){
                this.classList.remove('zero-opacity')
            }
        })
}


function fillTooltip(guid){
    const pitch = data.find((d)=>d.guid === guid);
    tooltipInfo = {
        'guid':guid,
        'desc':pitch.description ? pitch.description.split(".")[0] : null,
        'pitch_result': pitch.pitch_result,
        'batter':pitch.batter_name,
        'count':pitch.count,
        'pitch_speed':pitch.rel_speed,
        'pitch_type':pitch_types.find(d=>d.abbv===pitch.pitch_type).name,
        'exit_velocity':pitch.exit_velocity ? pitch.exit_velocity : null,
        'date':pitch.date
    };
}   

function emptyTooltip(){
    tooltipInfo = null;
}
    
</script>
    <div class="pitch_type_key">
        {#each pitch_types as type}
                {#if data.find((d)=>d.pitch_type===type.abbv)}
                <div class ="key_object">
                    <span class="dot" style={"background-color:"+type.color}></span><span>{type.name}</span>
                </div>
                {/if}
        {/each}
    </div>
    <div class ="pitch_scatter_container">
        <div class="options">
            <div class="dropdown_container">
                <div>Pitch Types</div>
                <select>
                    <option value="all" on:click={()=>{changePitch("all",'pitch_type')}}>All Pitches</option>
                    {#each pitch_types as type}
                        {#if data.find((d)=>d.pitch_type===type.abbv)}
                            <option value={type.name} on:click={()=>{changePitch(type.abbv,'pitch_type')}}>{type.name}</option>
                        {/if}
                    {/each}
                </select>
            </div>
            <div class="dropdown_container">
                <div>Batter Handedness</div>
                <select>
                    <option value="all" on:click={()=>{changePitch("all",'batter_side')}}>All Pitches</option>
                    <option value="left" on:click={()=>{changePitch("L", 'batter_side')}}>Left</option>
                    <option value="right" on:click={()=>{changePitch("R", 'batter_side')}}>Right</option>
                    
                </select>
            </div>
            <div class="dropdown_container">
                <div>Pitch Result</div>
                <select>
                    <option value="all" on:click={()=>{changePitch("all",'ball_call')}}>All Pitches</option>
                    <option value="in_play" on:click={()=>{changePitch("in_play",'ball_call')}}>Ball in play</option>
                    <option value="foul" on:click={()=>{changePitch("foul",'ball_call')}}>Foul</option>
                    <option value="all_strikes" on:click={()=>{changePitch("all_strikes", 'ball_call')}}>All Strikes</option>
                    <option value="called_strike" on:click={()=>{changePitch("called_strike", 'ball_call')}}>-----Called Strike</option>
                    <option value="swinging_strike" on:click={()=>{changePitch("swinging_strike", 'ball_call')}}>-----Swinging Strike</option>
                    <option value="ball" on:click={()=>{changePitch("ball", 'ball_call')}}>Ball</option>
                </select>
            </div>
        </div>
        <svg width={width} height={height}>
            <g class="scatter_circles" on:mouseleave={()=>{emptyTooltip()}}>
            {#each data as pitch}
                <circle
                    id={pitch.guid}
                    cx={scaleX(pitch.plate_x)}
                    cy={scaleY(pitch.plate_z)}
                    r={getLength(0.12,scaleX)}
                    opacity=1
                    fill={pitch_types.find((d)=>d.abbv == pitch.pitch_type).color}
                    style=""
                    data-pitch_type={pitch.pitch_type}
                    data-batter_side={pitch.batter_side}
                    data-ball_call={pitch.ball_call}
                    on:click={()=>{fillTooltip(pitch.guid)}}
                >
                </circle>
            {/each}
            </g>
            <!-- strikezone -->
            <rect 
                width={getLength(1.7,scaleX)}
                height={getLength(2.1,scaleY)}
                x={scaleX(-0.85)}
                y={scaleY(3.6)}
                fill=none
                style="stroke-width:1.5;stroke:black;" 
            >
            </rect>
        </svg>
        <div class="tooltip">
            {#if tooltipInfo}
                    <div style="max-width:300px;"><b>{tooltipInfo.desc ? tooltipInfo.desc : tooltipInfo.pitch_result}</b></div>
                    {#if !tooltipInfo.desc}
                        <div>vs. {tooltipInfo.batter}</div>
                    {/if}
                    <div>Count: {tooltipInfo.count}</div>
                    <div>Pitch Type: {tooltipInfo.pitch_type}</div>
                    <div>Pitch Speed: {tooltipInfo.pitch_speed} MPH</div>
                    {#if tooltipInfo.exit_velocity}
                        <div>Exit Velocity: {tooltipInfo.exit_velocity} MPH</div>
                    {/if}
                    <div>Date: {tooltipInfo.date}</div>
                    <div><a href={"https://baseballsavant.mlb.com/sporty-videos?playId="+tooltipInfo.guid} target="_blank" rel="noopener noreferrer">View Pitch</a></div>
            {:else}
                <div style="text-wrap: wrap">Click on a pitch for more info:</div>
            {/if}
        </div>
    </div>



<style>
    .pitch_scatter_container{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        color: black;
    }
    h2{
        text-align: left;
        margin-left: 0px;
    }
    select{
        text-align:right;
    }
    .options{
        text-align: right;
        margin-right: 10px;
        width: 250px;
    }
    .tooltip{
        text-align: left;
        width: 250px;
    }
    .dropdown_container{
        margin-bottom: 15px;
    }
    circle{
        stroke:black;
        stroke-width:1px;
    }
    .scatter_circles:hover circle{
        opacity:0.1;
    }
    .scatter_circles:hover circle:hover{
        cursor:pointer;
        stroke: black;
        stroke-width: 2px;
        opacity: 1;
        filter: saturate(2);
        
    }
    :global(.zero-opacity){
        opacity: 0 !important;
        pointer-events: none;
        cursor: default !important;
    }
    .pitch_type_key{
        display: flex;
        justify-content: center;
        align-items: center;
        column-gap: 10px;
        margin-bottom: 10px;
        font-size: 14px;
    }
    .dot {
        height: 12px;
        width: 12px;
        border-radius: 50%;
        display: inline-block;
        border: 1px solid black;
    }
    .key_object{
        display:flex;
        align-items: center;
        column-gap: 3px;
    }
</style>


