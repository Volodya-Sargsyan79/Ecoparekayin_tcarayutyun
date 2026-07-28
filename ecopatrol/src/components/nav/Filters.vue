<template>
    <div class="menu">
        <MenuItem 
            v-for="(item, index) in visibleMenuTree"
            :key="index"
            :label="item.label"
            :title="item.title"
            :func="item.func"
            :depth="0"
            :data="item.children"
        />
    </div>
</template>

<script>
    import axios from 'axios';
    import MenuItem from './MenuItem.vue';
    export default {
        name: 'Filters',
        data() {
            return {
                menuTree: [
                    {
                        label: 'ՀՀ Սյունիքի',
                        title: 'Ս',
                        regionId: 1,
                        func: () => this.searchShifth(1)
                    },
                    {
                        label: 'ՀՀ Կոտայք և Գեղարքունիք',
                        title: 'Կ',
                        regionId: 2,
                        func: () => this.searchShifth(2)
                    },
                    {
                        label: 'ՀՀ Տավուշ',
                        title: 'Տ',
                        regionId: 3,
                        func: () => this.searchShifth(3)
                    },
                    {
                        label: 'ՀՀ Լոռի',
                        title: 'Լ',
                        regionId: 4,
                        func: () => this.searchShifth(4)
                    },
                    {
                        label: 'ՀՀ Վայոց ձոր և Արարատ',
                        title: 'Վ',
                        regionId: 5,
                        func: () => this.searchShifth(5)
                    },
                    {
                        label: 'ՀՀ Շիրակ և Արագածոտն',
                        title: 'Շ',
                        regionId: 6,
                        func: () => this.searchShifth(6)
                    },
                    {
                        label: 'Երևան և ՀՀ Արմավիր',
                        title: 'Ե',
                        regionId: 7,
                        func: () => this.searchShifth(7)
                    }
                ],
                limit: 10,
                offset: 0
            }
        },
        components: {
            MenuItem
        },
        computed: {
            visibleMenuTree() {
                const user = this.$store.state.user
                const groups = user.groups || []

                // Տվյալները դեռ չեն բեռնվել
                if (user.isLoading || !groups.length) {
                    return []
                }

                const isDutyOfficer = groups.includes('Հերթապահներ')
                const isPrecinctHead = groups.includes('Տեղամասի պետեր')
                const isRegionHead = groups.includes('Վարչության պետեր')

                // Օպերատորը և ադմինը տեսնում են բոլոր վարչությունները
                if (
                    !isDutyOfficer &&
                    !isPrecinctHead &&
                    !isRegionHead
                ) {
                    return this.menuTree
                }

                const regionId = Number(user.region_id)

                if (!regionId) {
                    return []
                }

                // Հերթապահը, տեղամասի պետը և վարչության պետը
                // տեսնում են միայն իրենց վարչությունը
                return this.menuTree.filter(
                    region => Number(region.regionId) === regionId
                )
            }
        },
        methods: {
            searchShifth(e) {
                axios
                    .get('/api/ecopatrol/precinct/', {
                    params: { id: e }
                    })
                    .then((res) => {
                    const user = this.$store.state.user
                    const groups = user.groups || []
                    const precincts = res.data || []

                    const isDutyOfficer =
                        groups.includes('Հերթապահներ')

                    const isPrecinctHead =
                        groups.includes('Տեղամասի պետեր')

                    const isRegionHead =
                        groups.includes('Վարչության պետեր')

                    // Վարչության պետը տեսնում է տվյալ վարչության բոլոր տեղամասերը
                    if (isRegionHead) {
                        this.$store.state.user.precincts = precincts
                    }

                    // Հերթապահը և տեղամասի պետը տեսնում են միայն իրենց տեղամասը
                    else if (isDutyOfficer || isPrecinctHead) {
                        this.$store.state.user.precincts = precincts.filter(
                        precinct =>
                            Number(precinct.id) === Number(user.precinct_id)
                        )
                    }

                    // Ադմին, օպերատոր և այլ խմբեր
                    else {
                        this.$store.state.user.precincts = precincts
                    }

                    this.$router.push(
                        '/dashboard/precinct_shift/search_information/searchshift'
                    )
                    })
                    .catch((err) => {
                    console.error(err)
                    })
                },
            placeKeeper(e){
                axios
                .get('/api/ecopatrol/getstationshiftlist/', {
                    params: { id: e},
                }) 
                .then((res) => {
                    this.$store.state.user.stationshif = res.data;
                    this.$router.push('/dashboard/precinct_shift/information/shitlist') 
                })
                .catch(err => { console.error(err) }) 
            }
        }
    }
</script>

<style lang="scss" scoped>
    .menu {
        width: 100%;
        transition: all .3s ease;
        overflow: auto;
    }
</style>