<script>
import {scaleLinear} from "d3-scale";
import {trajectory_types} from "../assets/common_types"

export let data;

let pi = Math.PI;

function createBarrelPath(){
    let points = [[130,50], [116,50], [98,30], [98,26], [116,8], [130,8]];
    let final_string = "M";
    for (const point of points){
        let radian_angle = point[1]*(2*pi/360)
        let x_coord = scaleX(point[0]*Math.cos(radian_angle));
        let y_coord = scaleY(point[0]*Math.sin(radian_angle));
        final_string += (final_string === "" ? "C" : " ") + x_coord + " " + y_coord
    }
    return final_string + " Z";
}

let margin = {'left':50, 'top':45};

let width = 280 + margin.left ;
let height = 560 + margin.top ;

let scaleX = scaleLinear([0,130],[margin.left,width])
let scaleY = scaleLinear([130,-130],[margin.top,height])

function getLength(length,scale){
    return Math.abs(scale(length)-scale(0));
}

</script>

    <div class="barrel-container">
        <div class="arrow-legend">
            {#each Object.entries(trajectory_types) as [type,values]}
                <div><span style={"color:"+values.color+"; font-weight: bold; font-size: 20px; margin-right: 5px;"+values.color}>&uarr;</span>{values.title}</div>
            {/each}
        </div>
        <svg width={width} height={height}>
            <defs>
                <!-- different color markers -->
                <marker 
                id='arrow_ground_ball' 
                orient="auto" 
                markerWidth='8' 
                markerHeight='16' 
                refX='0.1' 
                refY='2'
                >
                <path d='M0,0 V4 L2,2 Z' fill={trajectory_types['ground_ball'].color} />
                </marker>
                <marker 
                id='arrow_fly_ball' 
                orient="auto" 
                markerWidth='2' 
                markerHeight='4' 
                refX='0.1' 
                refY='2'
                >
                <path d='M0,0 V4 L2,2 Z' fill={trajectory_types['fly_ball'].color} />
                </marker>
                <marker 
                id='arrow_line_drive' 
                orient="auto" 
                markerWidth='2' 
                markerHeight='4' 
                refX='0.1' 
                refY='2'
                >
                <path d='M0,0 V4 L2,2 Z' fill={trajectory_types['line_drive'].color} />
                </marker>
                <marker 
                id='arrow_popup' 
                orient="auto" 
                markerWidth='2' 
                markerHeight='4' 
                refX='0.1' 
                refY='2'
                >
                <path d='M0,0 V4 L2,2 Z' fill={trajectory_types['popup'].color} />
                </marker>
                <marker 
                id='arrow_bunt_grounder' 
                orient="auto" 
                markerWidth='2' 
                markerHeight='4' 
                refX='0.1' 
                refY='2'
                >
                <path d='M0,0 V4 L2,2 Z' fill={trajectory_types['bunt_grounder'].color} />
                </marker>
            </defs>

            <line x1={scaleX(0)} x2={scaleX(0)} y1={scaleY(-125)} y2={scaleY(125)} style={"stroke:#aaa;stroke-width:1;"}></line>
            <line x1={scaleX(-130)} x2={scaleX(130)} y1={scaleY(0)} y2={scaleY(0)} style={"stroke:#aaa;stroke-width:1;"}></line>
            
            <text text-anchor="middle" x={scaleX(0)} y={scaleY(139)}>Exit Velocity</text>
            <text text-anchor="middle" x={scaleX(0)} y={scaleY(130)}>(mph)</text>
            <text text-anchor="end" x={scaleX(-3)} y={scaleY(117)}>120</text>
            <text text-anchor="end" x={scaleX(-3)} y={scaleY(77)}>80</text>
            <text text-anchor="end" x={scaleX(-3)} y={scaleY(37)}>40</text>

            <path d={createBarrelPath()} class="barrel-zone"></path>
            {#each [120,80,40] as degree}
                <path class="axis-ellipses" d={"M "+ scaleX(0) +" "+ scaleY(degree)+ " A " + getLength(degree,scaleY) + " " + getLength(degree,scaleY) +" 0 1 1 " + scaleX(0) +" "+ scaleY(-1*degree)}
                >
                </path>
            {/each}
            <text text-anchor="start" x={270} y={-147.5} transform="rotate(60)" style="fill:black;font-weight:bold;">Barrel Zone</text>	
            <g>
                {#each data as contact}
                    {@const angle = contact.launch_angle*(2*pi/360)}
                    <path d={"M"+scaleX(0)+" "+scaleY(0)+" L"+(scaleX(Math.cos(angle)*contact.exit_velocity))+" "+(scaleY((Math.sin(angle)*contact.exit_velocity)))} 
                        class = "hit-arrow"
                        marker-end={'url(#arrow_'+contact.hit_trajectory+')'}
                        stroke={trajectory_types[contact.hit_trajectory].color}
                        stroke-width={4}
                        opacity=0.6
                        ></path>
                
                {/each}
            </g>
        </svg>
    </div>

    <style>
        .barrel-container{
            display:flex;
            column-gap: 20px;
        }
        .axis-ellipses{
            fill: none;
            stroke: #888;
            stroke-width: 1px;
        }
        .barrel-zone{
            fill: red;
            /* stroke: red; */
            opacity: 0.1;
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
        .arrow-legend{
            text-align: left;
            margin-top: 50px;
        }
    </style>