<script>
	import Router from 'svelte-spa-router';
  import Home from './routes/Home.svelte';
  import Pitcher from './routes/Pitcher.svelte';
  import Batter from './routes/Batter.svelte';
</script>

<main>
</main>

<Router routes={{
	'/': Home,
	'/pitcher': Pitcher,
	'/batter': Batter
}} />

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>