<script lang="ts">
import {scaleLinear, scaleSequential, scaleDiverging} from 'd3-scale';

export let data;

var margin = {top: 10, right: 30, bottom: 40, left: 50},
    width = 520 - margin.left - margin.right,
    height = 520 - margin.top - margin.bottom;

var scaleY = scaleLinear([5,0],[margin.bottom,height-margin.top]);
var scaleX = scaleLinear([-2.5,2.5],[margin.left,width-margin.right])

function getLength(length,scale){
    return Math.abs(scale(length)-scale(0));
}
    
</script>

<div>
    <svg width=520 height=520>
        <g>
        <!-- pitch overlay -->
        {#each data as pitch}
            <circle
                cx={scaleX(pitch.plate_x)}
                cy={scaleY(pitch.plate_z)}
                r={getLength(0.12,scaleX)}
                opacity={0.3}
                fill="orange"
                style="mix-blend-mode:multiply"
            >
            </circle>
        {/each}
        </g>
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


