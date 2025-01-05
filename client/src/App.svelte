<script>
  import { onMount } from 'svelte';

  let searchQuery = $state(null);
  let promise;
  let player = $state(null);

  // async function playerSearch(query){
  //   const response = await fetch('./player_search/'+query);
  //   const player = await response.json();
  //   return player['pitcher_name_last'];
  // }

  // function handleClick(query){
  //   promise = playerSearch(query);
  // }

  export function playerSearch(){
    event.preventDefault()
    fetch('./player_search/'+searchQuery)
      .then(d => d.text())
      .then(d => (player = d));
  }
     
</script>

<main>
  <form>
    <label>
      Last Name
      <input bind:value={searchQuery}>
    </label>
    <button on:click={() => playerSearch()}>Submit</button>
  </form>
  {#if player != null}
      <p>{player}</p>
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
</style>
