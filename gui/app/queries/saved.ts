function useSavedItemsQuery() {
  const { $api } = useNuxtApp()

  return useQueryWithAuth({
    key: ['me', 'saved-items'],
    query: () => $api('/v1/me/saved'),
  })
}

export { useSavedItemsQuery }
