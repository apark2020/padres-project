<script>
    import {scaleLinear} from "d3-scale";
    import { ticks } from 'd3-array';
    import Toggle from 'svelte-toggle';

    export let data;
    export let pitch_types;

    let isToggled = false;

    var margin = {top: 30, right: 20, bottom: 10, left: 20},
    width = 450 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

    var scaleY = scaleLinear([28,-28],[margin.bottom,height-margin.top]);
    var scaleX = scaleLinear([-28,28],[margin.left,width-margin.right]);

    let pitch_mvmt_averages;

    function getAverages(data){
        let pitchAggregates = data.reduce(function(accum,current){
            if(!accum[current.pitch_type]){
                accum[current.pitch_type]={
                    'induced_vert_break':current.induced_vert_break,
                    'horz_break':current.horz_break,
                    'count':1
                }
            }
            else{
                accum[current.pitch_type]['induced_vert_break'] += current.induced_vert_break;
                accum[current.pitch_type]['horz_break'] += current.horz_break;
                accum[current.pitch_type]['count'] += 1;
            }
            return accum;
        },{});

        let groupby = Object.entries(pitchAggregates).map(([key,value])=>({
            'pitch_type':key,
            'avg_vert_break':Math.round(10*value.induced_vert_break/value.count)/10,
            'avg_horz_break':Math.round(10*value.horz_break/value.count)/10,
            'count':value.count
            }));

        return groupby;
    }

    $: pitch_mvmt_averages = getAverages(data);

</script>

<div class="movement_container">
    <div class="toggle-cont">
        <div class="toggle-text" style="text-align: right;">Individual Pitches</div>
        <Toggle hideLabel on:toggle={(e) => (isToggled = e.detail)} />
        <div class="toggle-text" style="text-align: left;">Average</div>
    </div>
    <svg id ="movement-svg" width={width} height={height}>
        <defs>
            <marker 
              id='arrow_head' 
              orient="auto" 
              markerWidth='2' 
              markerHeight='4' 
              refX='0.1' 
              refY='2'
            >
              <path d='M0,0 V4 L2,2 Z' fill="#black" />
            </marker>
          </defs>
        <line x1={scaleX(-26)} x2={scaleX(26)} y1={scaleY(0)} y2={scaleY(0)} style={"stroke:#aaa;stroke-width:1;"}></line>
        <line x1={scaleX(0)} x2={scaleX(0)} y1={scaleY(-26)} y2={scaleY(26)} style={"stroke:#aaa;stroke-width:1;"}></line>
        <g id="x_axis">
            {#each ticks(-25,25,10) as tick}
                <line x1={scaleX(tick)} x2={scaleX(tick)} y1={scaleY(-0.5)} y2={scaleY(0.5)} style={"stroke:#aaa;stroke-width:1;"}></line>
                {#if (Math.abs(tick)%10 === 0) && (tick !== 0) }
                    <text class="label-text" text-anchor="middle" x={scaleX(tick)} y={scaleY(-2.5)} style="fill:#aaa;font-weight:bold;">{tick}{tick === -20 ? " in." : ""}</text>
                {/if}
            {/each}
        </g>
        <g id="y_axis">
            {#each ticks(25,-25,10) as tick}
                <line x1={scaleX(-0.5)} x2={scaleX(0.5)} y1={scaleY(tick)} y2={scaleY(tick)} style={"stroke:#aaa;stroke-width:1;"}></line>
                {#if (Math.abs(tick)%10 === 0) && (tick !== 0) }
                    <text class="label-text" text-anchor="start" x={scaleX(1)} y={scaleY(tick)+3} style="fill:#aaa;font-weight:bold;">{tick}{tick === -20 ? " in." : ""}</text>
                {/if}
            {/each}
        </g>
        <text class="label-text" text-anchor="middle" x={scaleX(0)} y={scaleY(27.5)} style="font-weight:bold;">Horizontal Movement</text>
        <text writing-mode="tb" class="label-text rotate" text-anchor="middle" x={scaleX(-27)} y={scaleY(0)} style="font-weight:bold;">Vertical Movement (Induced)</text>
        <g id="mvmt_points">
            {#if !isToggled}
                {#each data as pitch}
                        <circle
                            r=4
                            cx={scaleX(pitch.horz_break)}
                            cy={scaleY(pitch.induced_vert_break)}
                            fill={pitch_types.find((d)=>d['abbv']===pitch.pitch_type)['color']}
                            stroke="black"
                            stroke-width="1"
                            opacity=0.7
                        >
                        </circle>
                {/each}
            {:else}
                {#if pitch_mvmt_averages}
                    {#each pitch_mvmt_averages as pitch}
                        <circle
                            r={5*Math.pow(pitch.count,0.3)}
                            cx={scaleX(pitch.avg_horz_break)}
                            cy={scaleY(pitch.avg_vert_break)}
                            fill={pitch_types.find((d)=>d['abbv']===pitch.pitch_type)['color']}
                            stroke="black"
                            stroke-width="1"
                            opacity=0.7
                            style="mix-blend-mode:multiply;"
                        >
                        </circle>
                    {/each}
                {/if}
            {/if}
        </g>
        <g id="labels">
            <path d={"M"+scaleX(-17)+" "+scaleY(-25)+" L"+(scaleX(-25))+" "+(scaleY(-25))} 
                    marker-end='url(#arrow_head)'
                    stroke={'black'}
                    stroke-width={2}
                    opacity=0.7
                    ></path>
            <path d={"M"+scaleX(17)+" "+scaleY(-25)+" L"+(scaleX(25))+" "+(scaleY(-25))} 
                    marker-end='url(#arrow_head)'
                    stroke={'black'}
                    stroke-width={2}
                    opacity=0.7
                    ></path>
            <path d={"M"+scaleX(29)+" "+scaleY(1)+" L"+(scaleX(29))+" "+(scaleY(6))} 
                    marker-end='url(#arrow_head)'
                    stroke={'black'}
                    stroke-width={2}
                    opacity=0.7
                    ></path>
            <path d={"M"+scaleX(29)+" "+scaleY(-1)+" L"+(scaleX(29))+" "+(scaleY(-6))} 
                    marker-end='url(#arrow_head)'
                    stroke={'black'}
                    stroke-width={2}
                    opacity=0.7
                    ></path>
            <text class="label-text" text-anchor="end" x={scaleX(-16.5)} y={scaleY(-23.5)}>Towards 3B</text>
            <text class="label-text" text-anchor="start" x={scaleX(16.5)} y={scaleY(-23.5)}>Towards 1B</text>
            <text class="label-text" text-anchor="end" x={scaleX(27.5)} y={scaleY(4)}>More</text>
            <text class="label-text" text-anchor="end" x={scaleX(27.5)} y={scaleY(2)}>Rise</text>
            <text class="label-text" text-anchor="end" x={scaleX(27.5)} y={scaleY(-3)}>More</text>
            <text class="label-text" text-anchor="end" x={scaleX(27.5)} y={scaleY(-5)}>Drop</text>
        </g>
    </svg>
</div>

<style>
    .arrow-line {
        fill: gold;
        stroke: black;
        stroke-width: 6;
    }
    .label-text{
        font-size: 12px;
    }
    .toggle-cont{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        margin-bottom: 5px;
        column-gap: 10px;
    }
    .toggle-text{
        width: 100px;
        font-size: 14px;
        line-height: 1.25em;
    }
    .rotate{
        transform-box:fill-box;
        transform-origin: center;
        transform: rotate(180deg);
    }
</style>