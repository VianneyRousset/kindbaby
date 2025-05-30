<script setup lang="ts">
import { ShieldAlert } from 'lucide-vue-next'

// get user ID from route
const route = useRoute()
const router = useRouter()
const routeStack = useRouteStack()
const userId = Number.parseInt(route.params.user_id as string) // TODO avoid this hack

const { currentTab } = useTab()

// goto tab main page if invalid itemId
if (Number.isNaN(userId)) navigateTo(`/${currentTab}`)

// get main header bar height to offset content
const main = useTemplateRef<HTMLElement>('main')
const { height: mainHeaderHeight } = useElementSize(
  useTemplateRef('main-header'),
)

// current tab
const { currentTabRoot } = useTab()

// get user data
const { data: user } = useUserQuery(userId)

const { data: likedItems } = useLikedItemsQuery()
const { data: savedItems } = useSavedItemsQuery()

function openItem(itemId: number) {
  routeStack.amend(
    router.resolve({ ...route, hash: `#item${itemId}` }).fullPath,
  )
  return navigateTo(`${currentTabRoot}/item/${itemId}`)
}

// auth
const { loggedIn } = useAuth()
</script>

<template>
  <div>
    <!-- Header bar -->
    <AppHeaderBar
      ref="main-header"
      :scroll="main ?? false"
      :scroll-offset="32"
    >
      <div>
        <AppBack />
        <h1 :title="user?.name">
          {{ user?.name }}
        </h1>

        <!-- Dropdown menu -->
        <DropdownMenu v-if="loggedIn === true">
          <DropdownMenuItem class="red">
            <ShieldAlert
              style="cursor: pointer;"
              :size="32"
              :stroke-width="2"
            />
            <div>Signaler</div>
          </DropdownMenuItem>
        </DropdownMenu>
      </div>

      <div v-if="user">
        <UserAvatar :seed="user.avatar_seed" />
        <div class="counter">
          <div>{{ user.stars_count }}</div>
          <div>Étoiles</div>
        </div>
        <div class="counter">
          <div>{{ user.likes_count }}</div>
          <div>Likes</div>
        </div>
        <div class="counter">
          <div>{{ user.items.length }}</div>
          <div>Objects</div>
        </div>
      </div>
    </AppHeaderBar>

    <!-- Main content -->
    <main>
      <List
        v-if="user"
        ref="main"
        class="app-content page"
      >
        <ItemCard
          v-for="item in user.items"
          :id="`item${item.id}`"
          :key="`item${item.id}`"
          :item="item"
          :liked-items="likedItems ?? []"
          :saved-items="savedItems ?? []"
          @click="openItem(item.id)"
        />
        <ListEmpty v-if="user.items.length === 0">
          {{ user?.name }} n'a pas encore d'objet.
        </ListEmpty>
      </List>
    </main>
  </div>
</template>

<style scoped lang="scss">
main {
  --header-height: v-bind(mainHeaderHeight + "px");
}

:deep(.AppHeaderBar) {

  @include flex-column;
  align-items: stretch;
  padding: 0;
  gap: 0;
  height: 170px;

  &>div:first-child {
    @include flex-row;

    height: 64px;
    gap: 16px;
    padding: 0 1rem;

    h1 {
      @include ellipsis-overflow;
      flex-grow: 1;
      font-size: 1.6rem;
      font-weight: 500;
    }

  }

  &>div:last-child {
    @include flex-row;
    flex-grow: 1;
    justify-content: space-between;
    padding: 0 2rem;

    .counter {
      @include flex-column;

      &>div:first-child {
        font-size: 2rem;
        font-weight: 400;
        font-family: "Plus Jakarta Sans", sans-serif;
      }

      &>div:last-child {
        font-family: 'Inter', sans-serif;
        color: $neutral-400;
      }

    }

    gap: 16px;
    height: 64px;

    a {
      @include flex-row;
    }

    svg {
      stroke: $neutral-700;
    }

    h1 {
      @include ellipsis-overflow;
      flex-grow: 1;

      font-weight: 500;
      font-size: 1.6rem;
    }

  }
}

.main {
  padding-top: 170px;
  padding-bottom: 64px;
  box-sizing: border-box;
}
</style>
