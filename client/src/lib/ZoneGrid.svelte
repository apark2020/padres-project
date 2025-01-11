<script>
    import { schemeRdBu } from 'd3-scale-chromatic';
    import { scaleOrdinal } from 'd3-scale';

    import Toggle from 'svelte-toggle';
    export let batter_id;
    export let disciplineData;

    let isToggled = false;
    let sortedData;

    const color = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#f7f7f7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061'].reverse()

    function mapData(discData){
        return discData.map(function mapIt(d){
                    let x_zone = d.plate_x > 0.85 ? 'five' : d.plate_x >= 0.2833 ? 'four': d.plate_x >= -0.2833 ? 'three' : d.plate_x >= -0.85 ? 'two' : 'one';
                    let z_zone = d.plate_z > 3.6 ? 'five' : d.plate_z >= 2.9 ? 'four': d.plate_z >= 2.2 ? 'three' : d.plate_z >= 1.5 ? 'two' : 'one';
                    return{
                        ...d,
                        'x_zone':x_zone,
                        'z_zone':z_zone
                    }
                });
    }
    
    $: sortedData = mapData(disciplineData);
    
</script>
<div class="toggle-cont">
    <div class="toggle-text" style="text-align: right;">Swing%</div>
    <Toggle hideLabel on:toggle={(e) => (isToggled = e.detail)} />
    <div class="toggle-text" style="text-align: left;">Whiff%</div>
</div>
<div class="zone-full-container">
    <div class="zone-grid-container">
    {#key disciplineData}
        {#if sortedData}
            {#each ['one','two','three','four','five'] as col}
                <div class="column">
                    {#each ['one','two','three','four','five'] as row}
                    {@const filtered = sortedData.filter((d)=>(d.x_zone === row)&&(d.z_zone === col))}
                    {@const percentage = isToggled ? filtered.reduce((acc,curr)=>acc+curr.swinging_strike,0)/filtered.reduce((acc,curr)=>acc+curr.swing,0)*100 : filtered.reduce((acc,curr)=>acc+curr.swing,0)/filtered.length*100}
                        {#if percentage}
                                <div
                                    class = {"zone " 
                                        + (percentage > 90 || percentage < 20 ? 'white-text ' : '')
                                        + (['two','three','four'].includes(row) && ['two','three','four'].includes(col) ? 'outline' : '') 
                                        }
                                    style={"background-color:"+color[Math.floor(percentage/10)]}
                                >
                                {Math.round(percentage*10)/10}%    
                                </div>
                        {:else}
                            <div class="zone" style={"background-color:#ccc"}>N/A</div>
                        {/if}
                    {/each}
                </div>
            {/each}
        {/if}
    {/key}
    </div>
    <div class="zone-legend">
        {#each color.reverse() as hue, index}
            <div><span class="square" style={'background-color:'+hue}></span><span>{index === 0 ? '100' : (10-index)*10 +"-"+ ((10-index)*10+9)}%</span></div>
        {/each}
    </div>
</div>

<style>
.zone-grid-container{
    display:flex;
    margin: 0 auto;
    margin-top: 10px;
    width: 340px;
    height: 420px;
    
}
.square{
    background-color: blue;
}
.in_zone{
    border: 1px black;
}
.zone{
    min-width:68px;
    min-height:84px;
    stroke: #aaa;
    stroke-width: 1px;
    text-align:center;
}
.white-text{
    color: white;
}

.toggle-cont{
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
    margin-bottom: 10px;
    column-gap: 10px;
    }

.zone-full-container{
    display:grid;
    grid-template-columns: auto 30%;
    grid-gap: 25px;
}
.zone-legend{
    margin-top: 10px;
}
.zone-legend > div{
    display: flex;
    align-items: center;
    margin-left:0px;
}
.square {
    display: inline-block;
    height: 38px;
    width: 38px;
    margin-right: 5px;
    }
</style>