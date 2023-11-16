<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useI18n } from "vue-i18n";
import ScrollAnimate from "../App/ScrollAnimate.vue";
import process from "../../assets/images/home/process.svg?component";
import anime from "animejs";

const { t } = useI18n();
const progress = ref(0);

const t1 = anime.timeline({
  easing: "easeInOutSine",
  autoplay: false,
});

const taskElements = ref<(SVGUseElement | null)[]>([]);
const curveElements = ref<(SVGPathElement | null)[]>([]);
const textElements = ref<(SVGTextElement | null)[]>([]);
const textPathElements = ref<(SVGTextPathElement | null)[]>([]);
const circleElements = ref<(SVGCircleElement | null)[]>([]);
const circleNewElements = ref<(SVGCircleElement | null)[]>([]);
const axisElement = ref<SVGGElement | null>(null);
const learnwareCardBorderElements = ref<(SVGUseElement | null)[]>([]);
const learnwareCardElements = ref<(SVGGElement | null)[]>([]);

onMounted(() => {
  nextTick(() => {
    t1.add({
      targets: curveElements.value,
      keyframes: [
        { strokeDashoffset: 0, duration: 500 },
        {
          strokeDashoffset: (el: SVGPathElement): number => -Number(el.getAttribute("path-length")),
          duration: 300,
        },
      ],
      delay: anime.stagger(600),
    })
      .add(
        {
          targets: textElements.value,
          keyframes: [
            { opacity: 1, duration: 1 },
            { opacity: 1, duration: 499 },
            { opacity: 0, duration: 1 },
            { opacity: 0, duration: 499 },
          ],
          delay: anime.stagger(600),
        },
        "-=2000",
      )
      .add(
        {
          targets: textPathElements.value,
          startOffset: "100%",
          duration: 500,
          delay: anime.stagger(600),
        },
        "-=2200",
      )
      .add(
        {
          targets: circleElements.value,
          duration: 100,
          r: 8,
          delay: anime.stagger(600),
        },
        "-=1800",
      )
      .add({
        targets: axisElement.value,
        opacity: 0,
        duration: 1,
      })
      .add({
        targets: circleNewElements.value,
        keyframes: [
          { opacity: 1, duration: 1 },
          {
            cx: 1050,
            cy: (_el: SVGCircleElement, i: number): number => 300 * i + 140,
            r: 15,
            duration: 500,
          },
        ],
      })
      .add(
        {
          targets: taskElements.value,
          x: 450,
          duration: 500,
        },
        "-=500",
      )
      .add({
        targets: learnwareCardBorderElements.value,
        strokeDashoffset: 0,
        duration: 1000,
        delay: anime.stagger(700),
      })
      .add(
        {
          targets: learnwareCardElements.value,
          opacity: 1,
          duration: 500,
          delay: anime.stagger(700),
        },
        "-=1800",
      );
  });
});

function handleProgress(p: number): void {
  progress.value = p;

  t1.seek(t1.duration * p);
}

const vOffset = {
  mounted: (el: SVGPathElement): void => {
    const length = el.getTotalLength();
    el.style.strokeDasharray = String(length);
    el.style.strokeDashoffset = String(length);
    el.setAttribute("path-length", String(length));
  },
};
</script>

<template>
  <div class="md:py-30 mx-auto w-full max-w-[1200px] py-20 md:px-10">
    <div class="px-5 md:px-0">
      <div class="my-5 text-3xl lg:my-7 lg:text-4xl xl:my-10 xl:text-5xl">
        {{ t("Home.What.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.What.Description") }}
      </p>
    </div>

    <scroll-animate
      class="h-[1500vh]"
      @progress="handleProgress"
    >
      <div class="h-main-full flex flex-col items-center justify-center">
        <svg
          class="w-full"
          viewBox="0 0 1600 910"
        >
          <defs>
            <path
              id="path"
              transform="translate(0, 200)"
              d="M 0 0 S 400 0 800 300"
            />

            <clipPath id="task-clip">
              <rect
                x="0"
                y="0"
                width="500"
                height="200"
              />
            </clipPath>

            <process id="process" />
            <g id="task1">
              <use
                href="#process"
                y="-120"
              />
            </g>
            <g id="task2">
              <use
                href="#process"
                y="-370"
              />
            </g>
            <g id="task3">
              <use
                href="#process"
                y="-680"
              />
            </g>

            <marker
              id="arrow"
              viewBox="0 0 6 4"
              refX="3"
              refY="2"
              markerWidth="6"
              markerHeight="4"
              orient="auto"
              markerUnits="strokeWidth"
            >
              <path
                d="M 0 0 L 6 2 L 0 4 L 1 2 z"
                class="fill-gray-800"
              />
            </marker>

            <pattern
              id="star"
              viewBox="0,0,2 2"
            >
              <path
                d="M 0 0 L 2 0 L 2 2 L 0 2 z"
                class="fill-gray-800"
              />
              <path
                d="M 0 0 L 2 2 M 2 0 L 0 2"
                class="stroke-gray-800 stroke-[1]"
              />
            </pattern>

            <svg
              id="image"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 50 50"
              width="256px"
              height="256px"
            >
              <path
                d="M 0 5 L 0 29.585938 L 11.15625 18.429688 L 15.460938 24.890625 L 20.328125 23.914063 L 24.414063 28 L 30.320313 28 L 37.320313 33 L 50 33 L 50 5 Z M 37.5 14 C 39.433594 14 41 15.566406 41 17.5 C 41 19.433594 39.433594 21 37.5 21 C 35.566406 21 34 19.433594 34 17.5 C 34 15.566406 35.566406 14 37.5 14 Z M 10.84375 21.570313 L 0 32.414063 L 0 45 L 50 45 L 50 35 L 36.679688 35 L 29.679688 30 L 23.585938 30 L 19.671875 26.085938 L 14.539063 27.109375 Z"
              />
            </svg>
            <svg
              id="table"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="10 10 50 50"
              width="256px"
              height="256px"
            >
              <path
                d="M55 15c1.657 0 3 1.343 3 3v9H46V15H55zM52 23c1.104 0 2-.895 2-2 0-1.105-.896-2-2-2s-2 .895-2 2C50 22.105 50.896 23 52 23zM30 27V15h12v12H30zM36 19c-1.104 0-2 .895-2 2 0 1.105.896 2 2 2s2-.895 2-2C38 19.895 37.104 19 36 19zM14 18c0-1.657 1.343-3 3-3h9v12H14V18zM20 19c-1.104 0-2 .895-2 2 0 1.105.896 2 2 2s2-.895 2-2C22 19.895 21.104 19 20 19zM14 43V31h12v12H14zM20 35c-1.104 0-2 .895-2 2 0 1.105.896 2 2 2s2-.895 2-2C22 35.895 21.104 35 20 35zM14 56v-9h12v12h-9C15.343 59 14 57.657 14 56zM20 51c-1.104 0-2 .895-2 2 0 1.105.896 2 2 2s2-.895 2-2C22 51.895 21.104 51 20 51zM30 59V47h12v12H30zM46 59V47h12v9c0 1.657-1.343 3-3 3H46zM46 43V31h12v12H46zM30 43V31h12v12H30z"
              />
            </svg>

            <path
              id="download"
              d="M 20 0 v15 h-10 l15 15 15 -15 h-10 v-15 z M 10 35 h30 v5 h-30 z"
              transform="scale(0.6)"
            />

            <g
              id="learnware"
              opacity="1"
            >
              <rect
                x="0"
                y="0"
                width="770"
                height="290"
                rx="10"
                fill="white"
              />
              <text
                x="110"
                y="25"
                font-size="30"
                text-anchor="start"
                dominant-baseline="hanging"
              >
                Learnware
              </text>
              <text
                x="110"
                y="60"
                font-size="18"
                text-anchor="start"
                dominant-baseline="hanging"
                class="fill-gray-700"
              >
                Developer
              </text>
              <rect
                x="30"
                y="100"
                width="90"
                height="30"
                rx="3"
                class="fill-gray-400"
              />
              <rect
                x="140"
                y="100"
                width="150"
                height="30"
                rx="3"
                class="fill-gray-400"
              />
              <text
                x="215"
                y="115"
                font-size="20"
                class="fill-white"
                text-anchor="middle"
                dominant-baseline="middle"
              >
                Classification
              </text>

              <text
                x="30"
                y="170"
                font-size="25"
                class="fill-black"
                text-anchor="start"
                dominant-baseline="middle"
              >
                This is the description of a Learnware.
              </text>

              <text
                x="30"
                y="260"
                font-size="20"
                class="fill-gray"
                text-anchor="start"
                dominant-baseline="middle"
              >
                Updated Just Now
              </text>

              <use
                href="#download"
                x="720"
                y="240"
                width="30"
                height="30"
              />
            </g>
          </defs>

          <use
            v-for="i in 3"
            ref="taskElements"
            :key="i"
            :href="`#task${i}`"
            x="100"
            :y="300 * i - 250"
            clip-path="url(#task-clip)"
          />
          <g
            ref="axisElement"
            style="transform: skew(-9deg, -1deg)"
          >
            <path
              d="M 1100 600 h 350"
              class="fill-none stroke-gray-800 stroke-[6]"
              stroke-linecap="round"
              marker-end="url(#arrow)"
            />
            <path
              d="M 1150 670 v -350"
              class="fill-none stroke-gray-800 stroke-[6]"
              stroke-linecap="round"
              marker-end="url(#arrow)"
            />

            <circle
              v-for="i in 3"
              ref="circleElements"
              :key="i"
              :cx="[1320, 1285, 1325][i - 1]"
              :cy="[515, 540, 580][i - 1]"
              r="0"
              :class="['fill-blue-600', 'fill-green-800', 'fill-red-700'][i - 1]"
            />

            <text
              x="1290"
              y="720"
              font-size="30"
              text-anchor="middle"
            >Specification Space</text>
          </g>

          <circle
            v-for="i in 3"
            ref="circleNewElements"
            :key="i"
            :cx="[1238, 1200, 1233][i - 1]"
            :cy="[492, 518, 557][i - 1]"
            r="8"
            :class="['fill-blue-600', 'fill-green-800', 'fill-red-700'][i - 1]"
            opacity="0"
          />

          <path
            v-for="i in 3"
            :id="`curve${i}`"
            ref="curveElements"
            :key="i"
            v-offset
            :d="
              [
                'M 600 140 S1000 120 1220 480',
                'M 600 440 S1000 120 1180 500',
                'M 600 740 S1000 400 1220 540',
              ][i - 1]
            "
            class="fill-none stroke-[4]"
            :class="['stroke-blue-600', 'stroke-green-800', 'stroke-red-800'][i - 1]"
            stroke-linecap="round"
          />

          <text
            v-for="i in 3"
            ref="textElements"
            :key="i"
            :class="['fill-blue-600', 'fill-green-800', 'fill-red-700'][i - 1]"
            font-size="30"
            transform="translate(0, -20)"
            opacity="0"
          >
            <textPath
              ref="textPathElements"
              :href="`#curve${i}`"
              startOffset="0%"
              text-anchor="end"
              dominant-baseline="middle"
            >
              RKME Specification
            </textPath>
          </text>

          <g
            v-for="i in 3"
            ref="learnwareCardElements"
            :key="i"
            opacity="0"
          >
            <use
              x="400"
              :y="10 + 300 * (i - 1)"
              href="#learnware"
            />
            <use
              :href="['#image', '#table', '#table'][i - 1]"
              x="430"
              :y="30 + 300 * (i - 1)"
              width="60"
              height="60"
            />
            <text
              x="475"
              :y="125 + 300 * (i - 1)"
              font-size="20"
              class="fill-white"
              text-anchor="middle"
              dominant-baseline="middle"
            >
              {{ ["Image", "Table", "Table"][i - 1] }}
            </text>
          </g>

          <path
            v-for="i in 3"
            ref="learnwareCardBorderElements"
            :key="i"
            v-offset
            :d="`M 400 ${
              300 * (i - 1) + 20
            } a 10 10 0 0 1 10 -10 h750 a 10 10 0 0 1 10 10 v 270 a 10 10 0 0 1 -10 10 h-750 a 10 10 0 0 1 -10 -10 z`"
            class="fill-none stroke-black stroke-[2]"
          />
        </svg>
      </div>
    </scroll-animate>
  </div>
</template>
