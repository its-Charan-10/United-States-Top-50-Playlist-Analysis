import { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, Film, Users, DollarSign, Plus, Trash2, Edit } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { clsx } from 'clsx'

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('content')

  const stats = [
    { label: 'Total Users', value: '1,284', icon: <Users className="text-blue-500" /> },
    { label: 'Active Movies', value: '452', icon: <Film className="text-brand" /> },
    { label: 'Monthly Revenue', value: '$12,450', icon: <DollarSign className="text-green-500" /> },
  ]

  return (
    <div className="pt-24 min-h-screen px-4 md:px-12 bg-surface-overlay pb-20">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
        <div>
          <h1 className="text-4xl font-black mb-2">Admin Dashboard</h1>
          <p className="text-text-secondary">Manage content, users, and platform analytics.</p>
        </div>
        <button className="bg-brand hover:bg-brand-dark text-white px-6 py-2.5 rounded-lg font-bold flex items-center gap-2 transition-all">
          <Plus size={20} /> Upload New Content
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid sm:grid-cols-3 gap-6 mb-12">
        {stats.map((stat, idx) => (
          <div key={idx} className="glass-card p-6 rounded-2xl flex items-center gap-6">
            <div className="p-4 bg-white/5 rounded-2xl text-2xl">
              {stat.icon}
            </div>
            <div>
              <p className="text-text-secondary text-sm font-medium">{stat.label}</p>
              <p className="text-2xl font-black">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Main Content Area */}
      <div className="glass-card rounded-2xl overflow-hidden">
        <div className="flex border-b border-white/10">
          {['content', 'users', 'billing'].map((tab) => (
            <button 
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={clsx(
                "px-8 py-4 font-bold capitalize transition-all border-b-2",
                activeTab === tab ? "border-brand text-white bg-white/5" : "border-transparent text-text-secondary hover:text-white"
              )}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="p-6 overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-text-muted text-sm uppercase tracking-wider border-b border-white/5">
                <th className="pb-4 font-bold">Content</th>
                <th className="pb-4 font-bold">Category</th>
                <th className="pb-4 font-bold">Release</th>
                <th className="pb-4 font-bold">Rating</th>
                <th className="pb-4 font-bold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {[
                { title: 'Interstellar', type: 'Movie', year: '2014', rating: '8.6' },
                { title: 'Arcane', type: 'Series', year: '2021', rating: '9.0' },
                { title: 'Stranger Things', type: 'Series', year: '2016', rating: '8.7' },
                { title: 'The Witcher', type: 'Series', year: '2019', rating: '8.1' },
              ].map((item, idx) => (
                <tr key={idx} className="group hover:bg-white/2">
                  <td className="py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-12 aspect-video bg-surface-card rounded overflow-hidden">
                        <img src={`https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=100`} className="w-full h-full object-cover" />
                      </div>
                      <span className="font-medium">{item.title}</span>
                    </div>
                  </td>
                  <td className="py-4 text-text-secondary">{item.type}</td>
                  <td className="py-4 text-text-secondary">{item.year}</td>
                  <td className="py-4">
                    <span className="bg-green-500/10 text-green-500 px-2 py-0.5 rounded text-xs font-bold">
                      {item.rating}
                    </span>
                  </td>
                  <td className="py-4">
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button className="p-2 hover:bg-white/10 rounded-md text-text-secondary hover:text-white"><Edit size={16} /></button>
                      <button className="p-2 hover:bg-white/10 rounded-md text-text-secondary hover:text-red-500"><Trash2 size={16} /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
