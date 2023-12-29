import IconBallTennis from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/ball-tennis.tsx"

type Props = {
  active: string;
};


export function Header({ active }: Props) {
  const menus = [
    { name: "Home", href: "/" },
    { name: "Gallery", href: "/gallery" },
  ];

  return (
    <div class="bg-white w-full py-6 px-8 flex flex-col sm:flex-row items-center gap-4">
      <div class="flex items-center flex-1">
        <IconBallTennis aria-hidden="true" />
        <div class="text-2xl ml-1 font-bold">
          Temovre
        </div>
      </div>
      <ul class="flex items-center gap-6">
        {menus.map((menu) => (
          <li>
            <a
              href={menu.href}
              class={"text-gray-500 hover:text-gray-700 py-1 border-gray-500" +
                (menu.href === active ? " font-bold border-b-2" : "")}
            >
              {menu.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}