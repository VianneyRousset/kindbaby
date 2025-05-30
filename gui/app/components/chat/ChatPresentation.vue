<script setup lang="ts">
const props = defineProps<{
  me: User
  chat: Chat
}>()

const { me, chat } = toRefs(props)

// get messages
const { messages, loadMore, end } = useChatMessages(() => unref(chat).id)

// mutations
const { mutate: sendMessage } = useSendMessageMutation()

// chat input
const inputText = ref('')

// send message
async function submitMessage(msg: string) {
  await sendMessage({
    chatId: unref(chat).id,
    text: msg,
  })
  inputText.value = ''
}

const chatMessageInput = useTemplateRef<HTMLElement>('chat-message-input')
const { height: chatMessageInputHeight } = useElementSize(
  chatMessageInput,
  undefined,
  { box: 'border-box' },
)

const chatPresentation = useTemplateRef<HTMLElement>('chatPresentation')
useInfiniteScroll(
  chatPresentation,
  async () => {
    await loadMore()
  },
  {
    canLoadMore: () => !unref(end),
    distance: 1800,
  },
)
</script>

<template>
  <div
    ref="chatPresentation"
    class="ChatPresentation"
  >
    <ChatMessagesList
      :me="me"
      :chat="chat"
      :messages="messages"
    />
    <ChatMessageInput
      ref="chat-message-input"
      v-model="inputText"
      @submit="submitMessage"
    />
  </div>
</template>

<style lang="scss" scoped>
.ChatPresentation {

  @include flex-column;
  flex-direction: column-reverse;
  align-items: stretch;

  --chat-message-input-height: v-bind(chatMessageInputHeight + "px");

  padding-top: calc(var(--header-height) + 1rem);
  padding-bottom: calc(64px + var(--chat-message-input-height) + 1rem);

  .ChatMessageInput {
    position: absolute;
    bottom: calc(64px + 1rem);
    left: 0;
    right: 0;
  }
}
</style>
