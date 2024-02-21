import React, { useState } from 'react';

type Tab = {
  label: string;
  content: React.ReactNode;
};

interface TabsProps {
  tabs: Tab[];
}

const Tabs: React.FC<TabsProps> = ({ tabs }) => {
  const [activeTab, setActiveTab] = useState<number>(0);

  const changeTab = (index: number) => {
    setActiveTab(index);
  };

  return (
    <div>
      <div className="flex mb-4 space-x-4">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => changeTab(index)}
            className={`px-4 py-2 rounded ${
              activeTab === index
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div>{tabs[activeTab].content}</div>
    </div>
  );
};

export default Tabs;
