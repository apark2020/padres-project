<script>
    import Typeahead from "svelte-typeahead";
    import Barrel from '../lib/Barrel.svelte';
    import ZoneGrid from '../lib/ZoneGrid.svelte'
  
    const extract = (item) => item.first_name + " " + item.last_name + " (" + item.team + ")";
  
    let batter_data = $state(null);
    let current_batter_id;
    let disciplineData = $state(null);
   
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
          current_batter_id=query;
          fetch('./api/batter_record/'+query)
          .then(d => d.json())
          .then(d => (batter_data = d))
          .then(d => grabDisciplineData(query))
      }

      function grabDisciplineData(query){
          fetch('./api/batter_discipline/'+query)
              .then(d=>d.json())
              .then(d=>(disciplineData = d));
      }
  </script>

<nav>
	<a href="/">Home</a>
	<a href="/#/pitcher">Pitcher Analysis Tool</a>
	<a href="/#/batter">Batter Analysis Tool</a>
</nav>
  
  <main>
    {#await getBatters() then batters}
        <Typeahead 
            label="Type in a name" 
            data={batters} 
            showDropdownOnFocus
            limit={5}
            {extract}
            on:select={(e) => {
                batterSearch(e.detail.original.id);
            }}
        />
    {/await}
    {#if batter_data && disciplineData}
      <div class="charts">
        <div class="comp-container">
          <h2>Launch Angle/Exit Velocity</h2>
          <Barrel data={batter_data} />
        </div>
        <div class="comp-container">
          <h2>Plate Discipline</h2>
          <ZoneGrid batter_id={current_batter_id} {disciplineData} />
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
      column-gap: 40px;
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
  