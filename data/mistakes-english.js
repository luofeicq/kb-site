window.M_SUBJECT = 'english';
window.MISTAKES = [
{
  id: 'en01', topic: '时态语态', link: 'english-knowledge.html#e1', type: '客观题', source: '典型易错题', level: 2,
  q: 'When I got to the station, the train ______ (leave).',
  answer: 'had left',
  analysis: '"我到车站"用的是 got（一般过去时），而"火车离开"发生在"我到"之前，是"过去的过去"，所以用过去完成时 had left。\n判断口诀：句中已有一个过去时作参照，另一个发生得更早的动作用过去完成时。\n常见标志：by the end of last year、before + 过去动作、when + 过去动作（另一动作更早发生）。\n容易被误用的是"一般过去时"（left）——那样两个动作就变成同时或顺序发生，与句意不符。',
  points: ['过去的过去用过去完成时', '用已有的过去时作参照点', '与一般过去时区分']
},
{
  id: 'en02', topic: '非谓语', link: 'english-knowledge.html#e2', type: '客观题', source: '典型易错题', level: 3,
  q: '______ from the top of the tower, the city looks beautiful.',
  opts: ['A. Seen　B. Seeing　C. To see　D. Having seen'],
  answer: 'A',
  analysis: '判断三步：① 找非谓语的逻辑主语——主句主语是 the city；② 判断主动还是被动——城市是"被看"，是被动关系；③ 选形式——被动关系用过去分词 Seen。\n所以选 A。\n如果句意是"从塔顶看下去，我们看到城市很美"，逻辑主语变成 we，we 是主动"看"，就选 B. Seeing。\n这一类题的关键永远是先确定逻辑主语，再判断主动被动，不要凭语感。',
  points: ['先找逻辑主语', '主动 doing / 被动 done', '同一个空位随主语不同而变化']
},
{
  id: 'en03', topic: '定语从句', link: 'english-knowledge.html#e3', type: '客观题', source: '典型易错题', level: 2,
  q: 'This is the very book ______ I have been looking for.',
  opts: ['A. which　B. what　C. that　D. who'],
  answer: 'C',
  analysis: '先行词 book 被 the very 修饰，属于"只能用 that"的情形。\n此外，从句中 looking for 缺宾语，需要一个能作宾语的关系代词；what 不能引导定语从句（它不能指代先行词），who 只指人，所以 A 也不对。\n只能用 that 的情形记五条：① 先行词被 the very / the only / the same 修饰；② 被序数词修饰；③ 被最高级修饰；④ 先行词是 all / everything / nothing 等不定代词；⑤ 先行词同时包含人和物。\n另外：非限制性定语从句只能用 which，不能用 that。',
  points: ['the very 修饰时用 that', 'what 不能引导定语从句', '只能用 that 的五种情形']
},
{
  id: 'en04', topic: '情态动词', link: 'english-knowledge.html#e4', type: '客观题', source: '典型易错题', level: 3,
  q: '—I stayed up late last night to finish the report.\n—You ______ so late; the deadline is next Friday.',
  opts: ['A. needn\'t stay　B. needn\'t have stayed　C. mustn\'t stay　D. shouldn\'t stay'],
  answer: 'B',
  analysis: '"昨晚熬夜"这件事已经发生了，说话人表示"本来不必这样"，用 needn\'t have done，表示"做了但本来不需要"。\nA（needn\'t stay）是"现在/将来不必"，动作还没发生，与语境不符。\nC（mustn\'t stay）是"禁止"，语气完全不对。\nD（shouldn\'t stay）是"不应该（现在）"，也不指向已完成的动作。\n情态动词 + have done 的五种高频含义：\nmust have done 一定做过｜can\'t have done 不可能做过｜may have done 可能做过｜should have done 本该做却没做｜needn\'t have done 本不必做却做了。',
  points: ['情态动词 + have done 表示对过去的评价', 'needn\'t have done 的含义', '与 needn\'t do（现在）区分']
},
{
  id: 'en05', topic: '阅读七选五', link: 'english-knowledge.html#e5', type: '客观题', source: '典型易错题', level: 3,
  q: '阅读下面一段话，为空格处选择最合适的句子：\n"Reading aloud is one of the best ways to improve pronunciation. ______ It also helps you remember new words more easily."',
  opts: ['A. However, it takes a lot of time.',
         'B. Besides, it makes you more confident when speaking.',
         'C. Therefore, you should read silently instead.',
         'D. For example, many students dislike reading.'],
  answer: 'B',
  analysis: '空格后面紧跟的是 "It also helps…"——"also"说明前文已经列出了一个好处，空格处应当也是"另一个好处"，构成递进并列关系。\nB 提出"让你说话更自信"，是另一个好处，与后面的 "also" 完全衔接。\nA 是转折（缺点），与前后两个好处相悖。\nC 是结论，且与整段观点相反。\nD 是举例，但举的是负面情况，与"好处"的逻辑不一致。\n七选五的判断顺序：① 看空格位置（段中承接）→ ② 看前后逻辑词（also, however, therefore, for example）→ ③ 看代词指代（it / they / this 指代前文的什么）→ ④ 全部填完后通读检查。',
  points: ['逻辑词 also 提示并列递进', '空格位置决定句子的功能', '代词与指代一致性']
},
{
  id: 'en06', topic: '书面表达', link: 'english-knowledge.html#e6', type: '主观题', source: '典型易错题', level: 2,
  q: '改正下面句子中的错误：I very like playing basketball, and I also good at it.',
  answer: 'I like playing basketball very much, and I am also good at it.',
  analysis: '两处错误：\n① very like → like … very much。英语中 very 不能直接修饰动词，要用 very much，且通常放在句末。同类错误还有 "I very want to go"，应为 "I want to go very much"。\n② I also good at → I am also good at。good 是形容词，be good at 是系表结构，形容词前必须有系动词 be。\n这两类错误在写作中极为常见：副词位置错误、系动词遗漏。\n写完作文的检查清单：① 每个形容词前有没有 be 动词；② 动词的时态是否前后一致；③ 主谓是否一致；④ 有没有中英文直译的搭配（如 very like、open the light）。',
  points: ['very 不能修饰动词', '形容词前必须有系动词', '中英直译造成的搭配错误']
}
];
