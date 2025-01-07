<script>
  import { onMount } from 'svelte';
  import Typeahead from "svelte-typeahead";
  import Contour from './lib/Contour.svelte'
  import PitchScatter from './lib/PitchScatter.svelte'

  let pitcherList = [];
  let promise = new Promise(() => {});
  const extract = (item) => item.first_name + " " + item.last_name;


  let searchQuery = $state(null);
  let pitcher_data = $state(null);

  const getPitchers = async () => {
    const response = await fetch('./api/pitchers');
    const data = await response.json(); 
    return data.map((el)=>{
      return{
        'id':el.id,
        'first_name':el.first_name,
        'last_name':el.last_name
      }
    })
  }

  export function playerSearch(query){
    event.preventDefault()
    fetch('./api/player_record/'+query)
      .then(d => d.json())
      .then(d => (pitcher_data = d));
  }
     
</script>

<main>
  {#await getPitchers() then pitchers}
    <Typeahead 
      label="Look up a Padres pitcher" 
      data={pitchers} 
      {extract}
      on:select={(e) => {
        console.log(e.detail.original.id);
        playerSearch(e.detail.original.id);
      }}
     />
  {/await}
  <!-- <form>
    <label>
      Last Name
      <input bind:value={searchQuery}>
    </label>
    <button on:click={() => playerSearch()}>Submit</button>
  </form> -->
  <!-- {#if pitcher_data}
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Pitches</th>
        </tr>
      </thead>
      {#each pitcher_data as pitcher}
        <tr>
          <td>{pitcher.date}</td>
          <td>{pitcher.pitches}</td>
        </tr>
      {/each}
    </table>
  {/if} -->
  {#if pitcher_data}
    <div class='pitch_charts'>
      <!-- <Scatter data={pitcher_data.filter((d)=>d.pitch_type==='4S')} /> -->
        <PitchScatter data={pitcher_data} />
        <Contour data={pitcher_data} />
    </div>
  {/if}
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
  input {
      color: black;
  }
  :global([data-svelte-typeahead]) {
    color:black;
    :global(input){
      color: black;
    }
  }
  
  :global(.pitch_charts){
    display: grid;
    grid-template-columns: 50% auto;
  }
</style>
