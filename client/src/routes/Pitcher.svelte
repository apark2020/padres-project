<script>
    import Typeahead from "svelte-typeahead";
    import Contour from '../lib/Contour.svelte'
    import PitchScatter from '../lib/PitchScatter.svelte'
    import ScatterMovement from '../lib/ScatterMovement.svelte';
    import { pitch_types } from '../assets/common_types.js';
  
    const extract = (item) => item.first_name + " " + item.last_name + " (" + item.team + ")";
  
    let pitcher_data = $state(null);
  
    const getPitchers = async () => {
      const response = await fetch('./api/pitchers');
      const data = await response.json(); 
      return data.map((el)=>{
        return{
          'id':el.id,
          'first_name':el.first_name,
          'last_name':el.last_name,
          'team':el.team.split(" ").slice(-1)[0]
        }
      })
    }
  
    function playerSearch(query){
      event.preventDefault()
      fetch('./api/pitcher_record/'+query)
        .then(d => d.json())
        .then(d => (pitcher_data = d))
    }
    
  </script>

<nav>
	<a href="/">Home</a>
	<a href="/#/pitcher">Pitcher Analysis Tool</a>
	<a href="/#/batter">Batter Analysis Tool</a>
</nav>
  
  <main>
    {#await getPitchers() then pitchers}
      <Typeahead 
        label="Type in a name" 
        data={pitchers} 
        showDropdownOnFocus
        limit={5}
        {extract}
        on:select={(e) => {
          playerSearch(e.detail.original.id);
        }}
       />
    {/await}
    {#if pitcher_data}
      <div class='profile'>
      </div>
      <div class="charts">
          <div class="comp-container">
            <h2 style="margin-bottom: 10px;">Pitch-by-Pitch Data</h2>
            <PitchScatter data={pitcher_data} />
          </div>
          <div class="comp-container" id="border">
            <h2 style="margin-bottom: 5px;">Pitch Movement</h2>
            <ScatterMovement data={pitcher_data} {pitch_types}/>
          </div>
          <div class="comp-container">
            <h2>Breakdown by Pitch Type</h2>
            <Contour width={800} height={800} data={pitcher_data}/>
          </div>
      </div>
    {/if}
  
  </main>
  
  <style>
    input {
        color: black;
    }
    main{
      max-width: 100vw;
    }
    :global([data-svelte-typeahead]) {
      color:black;
      width:500px;
      :global(input){
        color: black;
      }
      margin-bottom: 30px;
    }
    .charts{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-evenly;
      /* column-gap: 20px; */
      /* row-gap: 20px; */
    }
    .comp-container{
      max-width: 900px;
      margin-bottom: 15px;
    }
    #border{
      border: 1px solid black;
    }
    
  </style>
  