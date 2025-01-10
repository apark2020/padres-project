<script>
  import { onMount } from 'svelte';
  import Typeahead from "svelte-typeahead";
  import Contour from './lib/Contour.svelte'
  import PitchScatter from './lib/PitchScatter.svelte'
  import ScatterMovement from './lib/ScatterMovement.svelte';
  import StrikeZoneGrid from './lib/StrikeZoneGrid.svelte';
  import { pitch_types } from './assets/pitch_types.js';

  const extract = (item) => item.first_name + " " + item.last_name + " (" + item.team + ")";

  let searchQuery = $state(null);
  let pitcher_data = $state(null);
  let current_pitcher;

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
    console.log('player searched');
    // current_pitcher = query;
    fetch('./api/player_record/'+query)
      .then(d => d.json())
      .then(d => (pitcher_data = d))
  }
     
</script>

<main>
  {#await getPitchers() then pitchers}
    <Typeahead 
      label="Look up a Padres pitcher" 
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
      <div class="comp-container">
        <h2>Pitch-By-Pitch Data</h2>
        <PitchScatter data={pitcher_data} />
      </div>
      <div class="comp-container">
        <h2>Breakdown by Pitch Type</h2>
        <Contour width={800} height={800} data={pitcher_data}/>
      </div>
        <!-- <ScatterMovement data={pitcher_data} {pitch_types}/> -->
        <!-- <StrikeZoneGrid data={pitcher_data} width={500} height={500} /> -->
    <!-- </div> -->
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
    margin-bottom: 50px;
  }
  .comp-container{
    max-width: 100vw;
  }
  
</style>
