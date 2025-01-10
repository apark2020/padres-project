<script>
    import {scaleLinear} from "d3-scale";

    export let data;
    export let pitch_types;

    var margin = {top: 10, right: 30, bottom: 40, left: 50},
    width = 400 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    var scaleY = scaleLinear([25,-25],[margin.bottom,height-margin.top]);
    var scaleX = scaleLinear([-25,25],[margin.left,width-margin.right]);


</script>

<div class="movement_container">
    <svg width={width} height={height}>
        <g class="points">
            {#each data as pitch}
                <circle
                    r=3
                    cx={scaleX(pitch.horz_break)}
                    cy={scaleY(pitch.induced_vert_break)}
                    fill={pitch_types.find((d)=>d['abbv']===pitch.pitch_type)['color']}
                    stroke="black"
                    stroke-width="1px"
                    opacity=0.8
                >
                </circle>
            {/each}
        </g>
    </svg>
</div>