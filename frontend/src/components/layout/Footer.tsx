import { useT } from "../../i18n";

export function Footer() {
  const t = useT();

  return (
    <footer className="border-t border-gray-200 bg-white py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <p className="text-sm text-gray-500">
            {t("footer.powered")}
          </p>
          <div className="flex gap-6">
            <a href="#" className="text-sm text-gray-400 hover:text-gray-600">
              {t("footer.about")}
            </a>
            <a href="#" className="text-sm text-gray-400 hover:text-gray-600">
              {t("footer.privacy")}
            </a>
            <a href="#" className="text-sm text-gray-400 hover:text-gray-600">
              {t("footer.terms")}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
