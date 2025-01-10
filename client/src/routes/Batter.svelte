<script>
    import Typeahead from "svelte-typeahead";
    import Barrel from '../lib/Barrel.svelte';
  
    const extract = (item) => item.first_name + " " + item.last_name + " (" + item.team + ")";
  
    let batter_data = $state(null);
   
      const getBatters = async () => {
          const response = await fetch('./api/batters');
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
  
      function batterSearch(query){
          event.preventDefault()
          fetch('./api/batter_record/'+query)
          .then(d => d.json())
          .then(d => (batter_data = d))
      }
  </script>

<nav>
	<a href="/">Home</a>
	<a href="/#/pitcher">Pitcher</a>
	<a href="/#/batter">Batter</a>
</nav>
  
  <main>
    {#await getBatters() then batters}
        <Typeahead 
            label="Look up a Batter" 
            data={batters} 
            showDropdownOnFocus
            limit={5}
            {extract}
            on:select={(e) => {
                batterSearch(e.detail.original.id);
            }}
        />
    {/await}
    {#if batter_data}
      <div class="charts">
        <div class="comp-container">
          <h2>Launch Angle/Exit Velocity</h2>
          <Barrel data={batter_data} />
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
      margin-bottom: 10px;
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
    h2{
      margin-bottom: 10px;
    }
  </style>
  